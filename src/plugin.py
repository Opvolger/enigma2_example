from Components.MenuList import MenuList
from Plugins.Plugin import PluginDescriptor
from Components.Label import Label
from Components.ActionMap import ActionMap
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from rtlxl import RtlXL


class HalloWorldScreen(Screen):
    skin = """
        <screen position="0,0" size="1280,720" title="RTLxl" >
            <!--<widget name="myLabel" position="10,60" size="200,40" font="Regular;20"/>-->
            <widget name="Menu" position="10,60" size="420,380" scrollbarMode="showOnDemand" />
        </screen>"""

    def __init__(self, session, args=None):
        self.rtlxl = RtlXL()
        self.session = session
        Screen.__init__(self, self.session)
        # self["myLabel"] = Label("Hello World ;-)")
        self["Menu"] = MenuList([])
        self["ActionMap"] = ActionMap(["SetupActions"],
                                      {
            "cancel": self.plugin_cancel,
            "ok": self.switch
        }, -1)
        self.show_overzicht()

    def plugin_cancel(self):
        if self.action == 'play':
            self.show_items(self.index_item)
        elif self.action == 'items':
            self.show_overzicht(self.index_overzicht)
        elif self.action == 'overzicht':
            self.close()  # add the RC Command "cancel" to close your Screen

    def switch(self):
        go_to_action = self["Menu"].getCurrent()[1]
        if go_to_action == 'items':
            self.index_overzicht = self["Menu"].getSelectionIndex()
            self.show_items()
        if go_to_action == 'play':
            self.index_item = self["Menu"].getSelectionIndex()
            self.show_play()

    def show_overzicht(self, select_index=None):
        self.action = 'overzicht'
        overzicht_items = self.rtlxl.get_overzicht()
        list_item = []
        for overzicht_item in overzicht_items:
            if overzicht_item.has_key('label'):
                label = overzicht_item['label'].encode('ascii', 'ignore')
                url = overzicht_item['url'].encode('ascii', 'ignore')
                list_item.append((label, 'items', url))
        self.url_items = None
        self["Menu"].setList(list_item)
        if select_index:
            self["Menu"].moveToIndex(select_index)

    def show_items(self, select_index=None):
        self.action = 'items'
        if self.url_items == None:
            self.url_items = self["Menu"].getCurrent()[2]
        a = 4
        video_items = self.rtlxl.get_items(self.url_items, False, 'adaptive')
        list_item = []
        for video_item in video_items:
            if video_item.has_key('label'):
                label = video_item['label'].encode('ascii', 'ignore')
                uuid = video_item['uuid'].encode('ascii', 'ignore')
                list_item.append((label, 'play', uuid))
        self.uuid_play = None
        self["Menu"].setList(list_item)
        if select_index:
            self["Menu"].moveToIndex(select_index)

    def show_play(self):
        self.action = 'play'
        if self.uuid_play == None:
            self.uuid_play = self["Menu"].getCurrent()[2]
        a = self.uuid_play
        b = 4


def start(session):
    session.open(HalloWorldScreen)
    #session.open(MessageBox, "Hello World!")


def Plugins(path, **kwargs):
    return [
        PluginDescriptor(
            name="Example", where=PluginDescriptor.WHERE_PLUGINMENU, fnc=start)
    ]
