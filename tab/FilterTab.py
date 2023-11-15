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

        self.ad = None
        self.filter_list = None

        ad_list = list(gv.filter_options_dict.keys())
        self.set_select_ad(ad_list[0])

        self.select_ad_widget = pn.widgets.Select(options=ad_list,
                                                  value=ad_list[0],
                                                  name='Type of signal')
        self.select_ad_widget.param.watch(self.set_select_ad, "value")

        self.select_type_widget = pn.widgets.Select(options=self.filter_list,
                                                    value=self.filter_list[0],
                                                    name='Type of filter')
        # self.imagen_pane = pn.panel("icon.png", width=60, height=60, align="center")

        # # Text widgets
        # self.text_title = pn.pane.Markdown("# Optimizer Viewer", style={'font-size': '16pt'})
        self.text_hint = pn.widgets.StaticText(name='Hint', value='')
        self.text_hint.value = self.select_ad_widget.value

        # # Input widgets
        # self.custom_input_widget = pn.widgets.TextInput(name='Custom function', visible=False)


        # # Checkbox widgets
        # self.seed_checkbox = pn.widgets.Checkbox(name='As random seed', visible=False, align='end')

        # # Button widgets
        # self.check_function_button.on_click(self.check_function)
        # self.optimize_button = pn.widgets.Button(name="Optimize", button_type="primary", visible=False)


        # Vars
        self.content = pn.Column(self.select_ad_widget,
                                 self.select_type_widget,
                                 self.text_hint.value, width=500)

    def set_select_ad(self, event):
        if isinstance(event, str):
            self.ad = event
            self.filter_list = gv.filter_options_dict[self.ad]
        else:
            self.ad = event.obj.value
            self.filter_list = gv.filter_options_dict[self.ad]
            self.select_type_widget.options = self.filter_list
            self.select_type_widget.value = self.filter_list[0]

