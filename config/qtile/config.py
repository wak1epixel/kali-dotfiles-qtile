import os
import subprocess
from libqtile import bar, hook, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

mod = "mod1"
terminal = "kitty"

colors = {
    "bg":       "#0d1b1e",
    "fg":       "#c3eaea",
    "accent":   "#00d9d9",
    "accent2":  "#ff5f7e",
    "inactive": "#4a6b6b",
}

@hook.subscribe.startup_once
def autostart():
    subprocess.run(["xset", "r", "rate", "250", "30"])
    subprocess.Popen(["picom", "-b"])
    subprocess.Popen([os.path.expanduser("~/.fehbg")])
    subprocess.Popen(["nm-applet"])

keys = [
    # Apps
    Key([mod], "Return", lazy.spawn(terminal), desc="Terminal"),
    Key([mod], "w", lazy.spawn("firefox"), desc="Firefox"),
    Key([mod], "e", lazy.spawn("thunar"), desc="Files"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc="Launcher"),
    Key([mod, "control"], "l", lazy.spawn("i3lock -c 0d1b1e"), desc="Lock"),
    Key([], "Print", lazy.spawn("flameshot gui"), desc="Screenshot"),

    # Window
    Key([mod], "q", lazy.window.kill(), desc="Close window"),
    Key([mod], "f", lazy.window.toggle_fullscreen(), desc="Fullscreen"),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Float"),

    # Focus
    Key([mod], "h", lazy.layout.left(), desc="Focus left"),
    Key([mod], "l", lazy.layout.right(), desc="Focus right"),
    Key([mod], "j", lazy.layout.down(), desc="Focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Focus next window"),

    # Move
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move up"),

    # Resize
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset sizes"),

    # Session
    Key([mod], "Tab", lazy.next_layout(), desc="Next layout"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Quit qtile"),
]

groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend([
        Key([mod], i.name, lazy.group[i.name].toscreen(), desc=f"Go to group {i.name}"),
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name, switch_group=True),
            desc=f"Move window to group {i.name}"),
    ])

layouts = [
    layout.Columns(border_focus="#7fc8ff", border_normal="#505050", border_width=3),
    layout.MonadTall(border_focus="#7fc8ff", border_normal="#505050", border_width=3),
    layout.Max(),
]

widget_defaults = dict(font="JetBrains Mono", fontsize=13, padding=4, foreground=colors["fg"],)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Spacer(length=10),
                widget.CurrentLayout(
                    foreground=colors["accent2"],
                    padding=6,
                ),
                widget.Sep(linewidth=1, padding=12,
                           foreground=colors["inactive"], size_percent=55),
                widget.GroupBox(
                    highlight_method="line",
                    highlight_color=[colors["bg"], colors["bg"]],
                    this_current_screen_border=colors["accent"],
                    active=colors["fg"],
                    inactive=colors["inactive"],
                    urgent_border=colors["accent2"],
                    padding=6,
                    disable_drag=True,
                ),
                widget.Sep(linewidth=1, padding=12,
                           foreground=colors["inactive"], size_percent=55),
                widget.Prompt(foreground=colors["accent"]),
                widget.WindowName(foreground=colors["fg"], max_chars=60),
                widget.Systray(padding=8),
                widget.Sep(linewidth=1, padding=12,
                           foreground=colors["inactive"], size_percent=55),
                widget.CPU(
                    format="  {load_percent}%",
                    foreground=colors["accent"],
                    padding=6,
                ),
                widget.Memory(
                    format="  {MemUsed:.0f}{mm}",
                    measure_mem="M",
                    foreground=colors["accent"],
                    padding=6,
                ),
                widget.Clock(
                    format="  %a %d %b   %I:%M %p",
                    foreground=colors["accent2"],
                    padding=6,
                ),
                widget.Spacer(length=10),
            ],
            28,
            background=colors["bg"],
            margin=[6, 8, 0, 8],
            opacity=0.9,
        ),
    ),
]
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False

floating_layout = layout.Floating(
    float_rules=[
        *layout.Floating.default_float_rules,
        Match(wm_class="ssh-askpass"),
        Match(title="pinentry"),
    ]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
focus_previous_on_window_remove = False
reconfigure_screens = True
auto_minimize = True

# Java UI toolkits check this against a whitelist of known-good WMs.
# Burp Suite is Java. Leave this alone.
wmname = "LG3D"
