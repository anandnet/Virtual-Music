colors = {
    "Light": {
        "BackgroundColor": [1, 0, 1, .2],
        "TabColor": [1, 0, 1, .3],
        "ThemeColor": [1, 0, 1, 1],
        "BottomStatusColor": [.9, 0.9, 1, .8],
        "PrimaryTextColor": [0, 0, 0, 1],
        "SecondaryTextColor": [0, 0, 0, .5],
        "SelectorHoverColor": [.7, .7, .7, .5],
        "SelectorActiveColor": [1, 0, 1, 1],
        "SelectorNormalColor": [1, 1, 1, .7]
    },
    "Dark": {
        "BackgroundColor": [0.05, 0.05, .05, 1],
        "TabColor": [0.05, 0.05, .05, .5],
        "ThemeColor": [1, 0, 1, 1],
        "BottomStatusColor": [1, 0, 1, .5],
        "PrimaryTextColor": [1, 1, 1, 1],
        "SecondaryTextColor": [1, 1, 1, .6],
        "SelectorHoverColor": [.3, .3, .3, .5],
        "SelectorActiveColor": [1, 0, 1, .5],
        "SelectorNormalColor": [.1, .1, .1, .3]
    }
}


def get_color(style, color_type):
    return colors[style][color_type]
