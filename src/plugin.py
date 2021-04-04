from Components.MenuList import MenuList
from Plugins.Plugin import PluginDescriptor
from Components.Label import Label
from Components.ActionMap import ActionMap
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from rtlxl import RtlXL
from enigma import eServiceReference


class HalloWorldScreen(Screen):
    skin = """
        <screen position="10,10" size="1260,700" title="RTLxl" >
            <!--<widget name="myLabel" position="10,60" size="200,40" font="Regular;20"/>-->
            <widget name="Menu" position="10,60" size="420,380" scrollbarMode="showOnDemand" />
        </screen>"""

    def __init__(self, session, args=None):
        self.rtlxl = RtlXL()
        self.video_type = "progressive"
        self.session = session
        Screen.__init__(self, self.session)
        # self["myLabel"] = Label("Hello World ;-)")
        self["Menu"] = MenuList([])
        self["ActionMap"] = ActionMap(["SetupActions"],
                                      {
            "cancel": self.plugin_cancel,
            "ok": self.switch
        }, -1)
        #self.show_overzicht()
        self.test()

    def plugin_cancel(self):
        self.show()
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
        video_items = self.rtlxl.get_items(self.url_items, False, self.video_type)
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

    def test(self):
        url = 'http://manifest.us.rtl.nl/rtlxl/v166/network/pc/adaptive/components/videorecorder/42/426250/426308/5cf65d84-a494-3f1c-adc7-60a9c1aaeff3.ssm/5cf65d84-a494-3f1c-adc7-60a9c1aaeff3.m3u8'
        url = 'http://resolver.streaming.api.nos.nl/livestream?url=/live/npo/tvlive/npo1/npo1.isml/npo1.m3u8'
        url = url.replace(':', '%3a')
        sref = eServiceReference("4097:0:1:0:0:0:0:0:0:0:%s" % url)
        try:
            # sref.play()
            self.session.nav.playService(sref, adjust=False)
            self.hide()
        except Exception:
            print("[SHOUTcast] Could not play %s" % sref)

    def show_play(self):
        self.action = 'play'
        self.session.nav.stopService()
        if self.uuid_play == None:
            self.uuid_play = self["Menu"].getCurrent()[2]
            self.play_name = self["Menu"].getCurrent()[0]
        url = self.rtlxl.movie_trans(self.uuid_play, self.video_type)
        url = url.replace('|','#')
        url = url.encode('ascii', 'xmlcharrefreplace')
        # url = 'http://resolver.streaming.api.nos.nl/livestream?url=/live/npo/tvlive/npo1/npo1.isml/npo1.m3u8'
        # https://forums.openpli.org/topic/33870-m3u8-in-bouquet/
        # https://forums.openpli.org//topic/31377-open-pli-en-m3u8-streams/
        # url = 'http://manifest.us.rtl.nl/rtlxl/v166/network/pc/adaptive/components/videorecorder/42/426250/426308/5cf65d84-a494-3f1c-adc7-60a9c1aaeff3.ssm/5cf65d84-a494-3f1c-adc7-60a9c1aaeff3.m3u8'
        url = url.replace(':', '%3a')
        # https://github.com/OpenPLi/enigma2-plugins/blob/95c0a5e674af2b3dca32cd888c19ace4140c71bd/shoutcast/src/plugin.py#L993
        # https://github.com/haroo/HansSettings/blob/3a25df90774b7dae80f4ba70d0ddae59e01ec0a0/e2_hanssettings_19e_23e_28e/userbouquet.stream_nieuws.tv
        #sref = eServiceReference(play_settings.get("stype", 4097), 0, toString(play_url))
        print(url)
        sref = eServiceReference("4097:0:1:0:0:0:0:0:0:0:%s" % url)
        try:
            sref.setName(self.play_name)
            # sref.play()
            self.session.nav.playService(sref, adjust=False)
            self.hide()
        except Exception:
            print("[SHOUTcast] Could not play %s" % sref)
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
