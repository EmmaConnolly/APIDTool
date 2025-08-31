from gi.repository import Gtk
from gramps.gen.const import GRAMPS_LOCALE as glocale
_ = glocale.translation.sgettext
from gramps.gen.db import DbTxn
from gramps.gen.lib import Citation, Source, Person, Family, Event
from gramps.gui.managedwindow import ManagedWindow
from gramps.gui.plug import tool
from gramps.gui.utils import ProgressMeter

class APIDTool(tool.BatchTool, ManagedWindow):

    # Mostly derived from mergecitations.py.
    def __init__(self, dbstate, user, options_class, name, callback=None):
        uistate = user.uistate
        self.user = user
        ManagedWindow.__init__(self, uistate, [], self.__class__)
        self.dbstate = dbstate
        self.set_window(Gtk.Window(), Gtk.Label(), "")
        tool.BatchTool.__init__(self, dbstate, user, options_class, name)
        if not self.fail:
            self.progress = ProgressMeter(_("Checking Sources"), "", parent=self.window)
            self.progress.set_pass(
                _("Looking for citation fields"), self.dbstate.db.get_number_of_citations()
            )
            uistate.set_busy_cursor(True)
            try:
                self.run()
            except:
                raise
            finally:
                self.progress.close()
                uistate.set_busy_cursor(False)

    # Some of the code in this method was copy-pasted from mergecitations.py
    def run(self):
        db = self.dbstate.db
        db.disable_signals()
        with DbTxn(_("Checking Sources"), db, batch=True) as trans:
            for handle in db.iter_source_handles():
                source = db.get_source_from_handle(handle)
                source_title = source.get_title()
                citation_handle_list = list(db.find_backlink_handles(handle))
                for class_name, citation_handle in citation_handle_list:
                    citation = db.get_citation_from_handle(citation_handle)
                    if len(citation.get_page()) == 0:
                        self.split_citation(db, trans, source, citation)
                    else:
                        for attribute in citation.get_attribute_list():
                            apid = citation.get_attribute_list()[0].get_value()
                            citation.set_page("{0} (APID: {1})".format(citation.get_page(), apid))
                            db.commit_citation(citation, trans)
                        self.progress.step()
        db.enable_signals()

    def split_citation(self, db, trans, source, citation):
        source_apid = ""
        for attribute in citation.get_attribute_list():
            if attribute.get_type() != "_APID":
                continue
            apid = attribute.get_value()
            title = apid.split('::')[0]
            if len(source_apid) == 0:
                source_apid = title
            if len(source.get_title()) == 0:
                source.set_title(title)
            if len(citation.get_page()) == 0:
                citation.set_page("APID: {0}".format(apid))
            else:
                new_citation = Citation()
                new_citation.set_page("APID: {0}".format(apid))
                if title == source_apid:
                    new_citation.source_handle = source.get_handle()
                else:
                    new_source = Source()
                    new_source.set_title(title)
                    new_citation.source_handle = db.add_source(new_source, trans)
                new_citation.add_attribute(attribute)
                new_citation_handle = db.add_citation(new_citation, trans)
                citation_ref_list = list(db.find_backlink_handles(citation.get_handle()))
                for class_name, object_handle in citation_ref_list:
                    if class_name == Person.__name__:
                        person = db.get_person_from_handle(object_handle)
                        person.add_citation(new_citation_handle)
                        db.commit_person(person, trans)
                    elif class_name == Event.__name__:
                        event = db.get_event_from_handle(object_handle)
                        event.add_citation(new_citation_handle)
                        db.commit_event(event, trans)
                    elif class_name == Family.__name__:
                        family = db.get_family_from_handle(object_handle)
                        family.add_citation(new_citation_handle)
                        db.commit_family(family, trans)
        db.commit_source(source, trans)
        db.commit_citation(citation, trans)


class APIDToolOptions(tool.ToolOptions):

    def __init__(self, name, person_id=None):
        tool.ToolOptions.__init__(self, name, person_id)
