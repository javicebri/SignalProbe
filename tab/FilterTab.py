import panel as pn
import holoviews as hv
import pandas as pd
import numpy as np
import GLOBAL_VARS as gv

hv.extension('bokeh')
pn.extension()

class FilterTab:
    def __init__(self):

        self.ad = None
        self.filter_list = None

        ad_list = list(gv.filter_options_dict.keys())
        frequency_units_list = list(gv.frequency_units_dict.keys())
        self.set_select_ad(ad_list[0])

        # Selector widgets
        self.select_ad_widget = pn.widgets.Select(options=ad_list,
                                                  value=ad_list[0],
                                                  name='Type of signal')
        self.select_ad_widget.param.watch(self.set_select_ad, "value")
        self.select_type_widget = pn.widgets.Select(options=self.filter_list,
                                                    value=self.filter_list[0],
                                                    name='Type of filter')

        self.select_cutoff_units_widget = pn.widgets.Select(options=frequency_units_list,
                                                            value=frequency_units_list[0],
                                                            align="end",
                                                            width=100)
        # self.imagen_pane = pn.panel("icon.png", width=60, height=60, align="center")

        # Text widgets
        self.text_hint = pn.widgets.StaticText(name='Hint', value='')
        self.text_hint.value = self.select_ad_widget.value

        # Input widgets
        self.cutoff_input_widget = pn.widgets.FloatInput(name='Cutoff frequency',
                                                         visible=True,
                                                         width=150)

        # # Checkbox widgets
        # self.seed_checkbox = pn.widgets.Checkbox(name='As random seed', visible=False, align='end')

        # Button widgets
        self.calculate_button = pn.widgets.Button(name="Calculate", button_type="primary", visible=True)
        self.calculate_button.on_click(self.calculate_function)


        # Vars
        self.content = pn.Column(self.select_ad_widget,
                                 self.select_type_widget,
                                 pn.Row(self.cutoff_input_widget,
                                        self.select_cutoff_units_widget),
                                 self.calculate_button,
                                 self.text_hint.value,
                                 width=500)

    def set_select_ad(self, event):
        if isinstance(event, str):
            self.ad = event
            self.filter_list = gv.filter_options_dict[self.ad]
        else:
            self.ad = event.obj.value
            self.filter_list = gv.filter_options_dict[self.ad]
            self.select_type_widget.options = self.filter_list
            self.select_type_widget.value = self.filter_list[0]

    def calculate_function(self, event):
        pass

