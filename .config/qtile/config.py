import subprocess
from pathlib import Path

from libqtile import bar, layout, widget, hook
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

from custom.themes import gruvbox_dark as gb

mod = "mod4"
terminal = "alacritty"
browser = "firefox-esr"


wp_size = 6
wp_icon = ""

groups = []
for num in range(wp_size):
    groups.append(Group(name=str(num + 1), label=wp_icon))

keys = [
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right",
    ),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key(
        [mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"
    ),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod, "control"], "i", lazy.layout.grow()),
    Key([mod, "control"], "m", lazy.layout.shrink()),
    Key([mod, "control"], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    Key([mod], "w", lazy.spawn(browser), desc="Launch browser"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "t",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window",
    ),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

for i in groups:
    keys.extend(
        [
            # mod1 + letter of group = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + letter of group = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod1 + shift + letter of group = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.MonadTall(
        border_focus=gb["blue"],
        border_normal=gb["bg0"],
        border_on_single=False,
        border_width=3,
        insert_position=1,
        margin=6,
        single_border_width=0,
        single_margin=6,
    ),
    layout.Columns(
        border_focus=gb["blue"],
        border_focus_stack=gb["blue"],
        border_normal=gb["bg0"],
        border_normal_stack=gb["bg0"],
        border_on_single=False,
        border_width=3,
        insert_position=1,
        margin=6,
        margin_on_single=6,
    ),
    layout.Max(border=0, margin=6),
]

widget_defaults = dict(
    font="JetBrainsMono Nerd Font Mono Bold",
    fontsize=12,
    padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        wallpaper="~/Pictures/wallpapers/bird.jpg",
        wallpaper_mode="fill",
        top=bar.Bar(
            size=30,
            background=gb["bg4"],
            border_width=0,
            margin=[12, 12, 0, 12],
            widgets=[
                widget.Spacer(length=9, background=gb["bg0_h"], foreground=gb["fg"]),
                widget.TextBox(
                    "󰌽",
                    background=gb["bg0_h"],
                    foreground=gb["fg"],
                    fontsize=21,
                    padding=0,
                ),
                widget.Spacer(length=9, background=gb["bg0_h"], foreground=gb["fg"]),
                widget.TextBox(
                    "",
                    background=gb["bg0"],
                    foreground=gb["bg0_h"],
                    fontsize=30,
                    padding=0,
                ),
                widget.Spacer(length=9, background=gb["bg0"]),
                widget.CurrentLayoutIcon(
                    background=gb["bg0"],
                    foreground=gb["fg"],
                    scale=0.5),
                widget.Spacer(length=12, background=gb["bg0"]),
                widget.GroupBox(
                    background=gb["bg0_s"],
                    fontsize=21,
                    highlight_method="text",
                    active=gb["fg"],
                    inactive=gb["gray0"],
                    this_current_screen_border=gb["yellow"],
                    this_screen_border=gb["yellow"],
                    disable_drag=True,
                    use_mouse_wheel=False,
                ),
                widget.TextBox(
                    background=gb["bg2"],
                    foreground=gb["bg0_s"],
                    fmt="",
                    fontsize=30,
                    padding=0,
                ),
                widget.WindowName(
                    background=gb["bg2"],
                    foreground=gb["fg"],
                ),
                widget.Spacer(length=12, background=gb["bg2"]),
                # widget.TextBox(
                #     background=gb["bg4"],
                #     foreground=gb["bg2"],
                #     fmt="",
                #     fontsize=30,
                #     padding=0,
                # ),
                widget.TextBox(
                    background=gb["bg2"],
                    foreground=gb["bg0_s"],
                    fmt="",
                    fontsize=30,
                    padding=0,
                ),
                widget.Systray(
                    background=gb["bg0_s"],
                    foreground=gb["fg"],
                ),
                widget.Spacer(
                    length=9,
                    background=gb["bg0_s"],
                ),
                widget.Volume(
                    background=gb["bg0_s"],
                    foreground=gb["fg"],
                ),
                widget.Spacer(
                    length=9,
                    background=gb["bg0_s"],
                ),
                widget.TextBox(
                    background=gb["bg0_s"],
                    foreground=gb["bg0_h"],
                    fmt="",
                    fontsize=30,
                    padding=0,
                ),
                widget.TextBox(
                    background=gb["bg0_h"],
                    foreground=gb["fg"],
                    fmt="",
                    fontsize=18,
                ),
                widget.Clock(
                    background=gb["bg0_h"],
                    foreground=gb["fg"],
                    format="%H:%M %a %Y-%m-%d",
                ),
                widget.Spacer(
                    length=9,
                    background=gb["bg0_h"],
                ),
            ],
        ),
        bottom=bar.Gap(6),
        right=bar.Gap(6),
        left=bar.Gap(6),
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position(),
    ),
    Drag(
        [mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()
    ),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "Qtile"


@hook.subscribe.startup_once
def autostart():
    script = "~/.config/qtile/autostart.sh"
    subprocess.run([script], shell=True)
