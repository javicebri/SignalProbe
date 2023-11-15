import panel as pn
import holoviews as hv
import pandas as pd
import numpy as np
import GLOBAL_VARS as gv
from tab import FilterTab
from tab import ChokeTab


hv.extension('bokeh')
pn.extension()

class SigProbe:
    def __init__(self):
        self.plot_pane = pn.pane.HoloViews()

        # self.imagen_pane = pn.panel("icon.png", width=60, height=60, align="center")

        self.text_title = pn.pane.Markdown("# SigProbe", style={'font-size': '16pt'})

        # Vars
        self.filter_tab = FilterTab.FilterTab()
        self.choke_tab = pn.Column()

    def view(self):
        return pn.Column(
            self.text_title,
            pn.Tabs(
                ("Filter", self.filter_tab.content),
                ("Choke", self.choke_tab),
            )
        )


app = SigProbe()
# Open app
app.view().servable(title="SigProbe")
