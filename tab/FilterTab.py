import panel as pn
import holoviews as hv
import pandas as pd
import numpy as np
import GLOBAL_VARS as gv

hv.extension('bokeh')
pn.extension()

class FilterTab:
    def __init__(self):
        # Selector widgets
        self.select_ad_widget = pn.widgets.Select(options=list(gv.filter_options_dict.keys()),
                                                  name='Type of signal')
        # self.select_method_widget.param.watch(self.set_method, "value")

        # self.imagen_pane = pn.panel("icon.png", width=60, height=60, align="center")

        # # Text widgets
        # self.text_title = pn.pane.Markdown("# Optimizer Viewer", style={'font-size': '16pt'})
        # self.text_hint = pn.widgets.StaticText(name='Hint', value='')
        self.text_title = pn.pane.Markdown("# SigProbe", style={'font-size': '16pt'})


        # # Input widgets
        # self.custom_input_widget = pn.widgets.TextInput(name='Custom function', visible=False)


        # # Checkbox widgets
        # self.seed_checkbox = pn.widgets.Checkbox(name='As random seed', visible=False, align='end')

        # # Button widgets
        # self.check_function_button.on_click(self.check_function)
        # self.optimize_button = pn.widgets.Button(name="Optimize", button_type="primary", visible=False)


        # Vars
        self.content = pn.Column(self.select_ad_widget, width=500)
