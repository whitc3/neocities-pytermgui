# whitc3, 2023

import json
import neocities
import pytermgui as ptg
import sys
import os


isAuth = False

nc = neocities.NeoCities()

# button-related functions

# HACK: so pyright says that i'm having a type issue here. too bad! it works.

def exitMacro(isGlobal: bool=True, manager: ptg.WindowManager=None, window: ptg.Window or ptg.Container=None): # type: ignore
    if manager is None or window is None:
        isGlobal = True
    if isGlobal == True:
        exit()
    else:
        manager.remove(window, animate=False)

def windowAddMacro (window: ptg.Window, manager: ptg.WindowManager, slotIndex: int=None, title: str=None): #type: ignore
    manager.add(window, assign=False, animate=False)
    if type(slotIndex) == int:
        manager.layout.assign(window, index=slotIndex)
    if type(title) == str:
        window.set_title(title)

def buttonPing(manager: ptg.WindowManager):
    '''Function that the ping button calls'''

    # prompt user for site
    siteInput = ptg.InputField(prompt="site> ")
    pingPrompt = ptg.Window(
            "",
            siteInput,
            "",
            ptg.Button("confirm", onclick=lambda *_: pingNeocities(manager, siteInput.value)),
            ptg.Button("back", onclick=lambda *_: exitMacro(False, manager, pingPrompt))
            )
    windowAddMacro(pingPrompt, manager, title="ping site")
    pingPrompt.center()
    pingPrompt.select(0)

    # function that the prompt calls
    def pingNeocities(manager: ptg.WindowManager, sitePing: str):
        '''Function that contacts the Neocities API'''

        # if the site has tags, this will get them
        def getTagList(si: dict) -> ptg.Container:
            '''Function that returns a tag list in the form of a container'''
            if len(si["tags"])>=1:
                tagList = ptg.Container("[italic surface+1]tags[/]")
                for i in si["tags"]:
                    tagList.__iadd__(ptg.Label(str(i)))

                tagFinal = tagList
            else:
                return ptg.Container(ptg.Label("[italic surface+1]no tags found[/]"))
            return tagFinal

        # one less loose end
        exitMacro(False, manager, pingPrompt)

        pingResponse = ptg.Window(ptg.Label(f"[italic surface+1]pinging [surface+2]{sitePing}[surface+1]...[/]"), box="SINGLE")
        windowAddMacro(pingResponse, manager, 3, "ping result")

        # we have a site? cool
        try:
            # get siteinfo, the prompt'll pass it to param "site"
            siteQuery = nc.info(sitePing)
            siteInfo = siteQuery["info"]

            # print in window
            pingResponse = ptg.Window(
                    ptg.Label(f"[italic surface+1]pinging [surface+2]{sitePing}[surface+1]...[/]"),
                    "[bold italic success]ping success[/]",
                    "",
                    ptg.Label(f'[bold]{siteInfo["sitename"]}[/]', parent_align=0),
                    ptg.Label(f'[italic accent+1 underline ~https://{siteInfo["sitename"]}.neocities.org]https://{siteInfo["sitename"]}.neocities.org[/]', parent_align=0),
                    getTagList(siteInfo),
                    ptg.Splitter(ptg.Label('[italic surface+1]hits[/]',parent_align=1), ptg.Label('[italic surface+1]views[/]',parent_align=1)),
                    ptg.Splitter(ptg.Label(str(siteInfo["hits"])), ptg.Label(str(siteInfo["views"]))),
                    "",
                    ptg.Label('[italic surface+1]created[/]'), ptg.Label(str(siteInfo["created_at"])),
                    "",
                    ptg.Label('[italic surface+1]last updated[/]'), ptg.Label(str(siteInfo["last_updated"])),
                    box="SINGLE"
                )

        # we don't have a site? fallback
        except nc.InvalidRequestError as ire:
            pingResponse = ptg.Window(
            ptg.Label(f"[italic surface+1]pinging [surface+2]{sitePing}[surface+1]...[/]"),
            "[bold italic error]ping fail[/]",
            "",
            ptg.Label(f"[italic error]raised error code {ire.status_code}[/]"),
            # HACK: we can do this better! i just don't know how, but it works anyway
            ptg.Label(f"[italic error-2]{json.loads(ire.reason)['message']}[/]"), # type: ignore
            box="SINGLE"
        )

        windowAddMacro(pingResponse, manager, 3, "ping result")
        manager.focus(index)

# TODO: implement authentication

def buttonAuth(manager: ptg.WindowManager):
    authPrompt = ptg.Window(
            ptg.KeyboardButton("api key", bound="a", onclick=lambda *_: promptAuth(manager, True)),
            "",
            ptg.KeyboardButton("user & pass", bound="u", onclick=lambda *_: promptAuth(manager, False)),
            "",
            "",
            ptg.KeyboardButton("back", bound="b", onclick=lambda *_: exitMacro(False, manager, authPrompt)),
            )
    windowAddMacro(authPrompt, manager, title="auth with")
    authPrompt.center()
    manager.focus(authPrompt)

    def promptAuth(manager: ptg.WindowManager, apiKey: bool):
        if apiKey == True:
            manager.toast("[error]this isn't implemented yet[/]", duration=1)
        else:
            manager.toast("[error]this isn't implemented yet[/]", duration=1)

with ptg.WindowManager() as manager:
    # if this shows, something's wrong
    index = ptg.Window("something happened? damn.")

    # drawing the initial layout
    if isAuth == False:
        index = ptg.Window(
                        "[bold accent]neocities terminal interface[/]",
                        "[surface+1]whitc3, 2023[/]",
                        "",
                        ptg.KeyboardButton("auth", index=0, bound="a", onclick=lambda *_:buttonAuth(manager)), 
                        "[italic surface+1]Authenticates with Neocities [/ italic error]! NOT IMPLEMENTED ![/]",
                        "",
                        ptg.KeyboardButton("ping", index=0, bound="p", onclick=lambda *_:buttonPing(manager)), 
                        "[surface+1 italic]Pings a Neocities site[/]",
                        "",
                        ptg.KeyboardButton("quit", index=0, bound="q", onclick=lambda *_:exitMacro()), 
                        "[surface+1 italic]Exits the program[/]",
                        box="SINGLE"
                    )
    else:
        index = ptg.Window(
                        "[bold accent]neocities terminal interface[/]",
                        "[surface+1]whitc3, 2023[/]",
                        "",
                        ptg.KeyboardButton("auth", index=0, bound="a", onclick=lambda *_:buttonAuth(manager)), 
                        "[surface+1 italic]Authenticates with Neocities[/]",
                        "",
                        ptg.KeyboardButton("ping", index=0, bound="p", onclick=lambda *_:buttonPing(manager)), 
                        "[surface+1 italic]Pings a Neocities site[/]",
                        "",
                        ptg.KeyboardButton("quit", index=0, bound="q", onclick=lambda *_:exitMacro()), 
                        "[surface+1 italic]Exits the program[/]",
                        box="SINGLE"
                    )
    manager.layout.add_slot("Header", height=1) # 0
    manager.layout.add_break()
    manager.layout.add_slot("Body left", width=0.25) # 1
    manager.layout.add_slot("Body") # 2
    manager.layout.add_slot("Body right", width=0.25) # 3
    manager.layout.add_break()
    manager.layout.add_slot("Footer", height=1) # 4
    manager.add(index, animate=False)
    manager.layout.assign(index, index=2)
    manager.layout.assign(ptg.Label('dotcities'), index=0)
