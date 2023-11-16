import panel as pn
import holoviews as hv
import pandas as pd
import numpy as np
import GLOBAL_VARS as gv

from model.filter import Filter, Butterwoth, route_filter_class

hv.extension('bokeh')
pn.extension()

class FilterTab:
    def __init__(self):

        self.ad = None
        self.filter_list = None
        self.filter_obj = None
        self.plot_pane = pn.pane.HoloViews()

        ad_list = list(gv.filter_options_dict.keys())
        frequency_units_list = list(gv.frequency_units_dict.keys())
        self.set_select_ad(ad_list[0])

        # Selector widgets
        self.select_ad_widget = pn.widgets.Select(options=ad_list,
                                                  value=ad_list[0],
                                                  name='Type of signal',
                                                  width=180)
        self.select_ad_widget.param.watch(self.set_select_ad, "value")
        self.select_type_widget = pn.widgets.Select(options=self.filter_list,
                                                    value=self.filter_list[0],
                                                    name='Type of filter',
                                                    width=180)

        self.select_cutoff_units_widget = pn.widgets.Select(options=frequency_units_list,
                                                            value=frequency_units_list[0],
                                                            align="end",
                                                            width=60)
        # self.imagen_pane = pn.panel("icon.png", width=60, height=60, align="center")

        # Text widgets
        self.text_hint = pn.widgets.StaticText(name='Hint', value='')
        self.text_hint.value = self.select_ad_widget.value

        # Input widgets
        self.cutoff_input_widget = pn.widgets.FloatInput(name='Cutoff frequency',
                                                         visible=True,
                                                         width=100)
        self.order_input_widget = pn.widgets.IntInput(name='Order',
                                                         visible=True,
                                                         width=100)

        # # Checkbox widgets
        # self.seed_checkbox = pn.widgets.Checkbox(name='As random seed', visible=False, align='end')

        # Button widgets
        self.calculate_button = pn.widgets.Button(name="Calculate", button_type="primary", visible=True)
        self.calculate_button.on_click(self.calculate_filter)
        self.text_hint.value = 'OBJETO MO CREADO'
        # Vars
        self.content = pn.Column(self.select_ad_widget,
                                 self.select_type_widget,
                                 pn.Row(self.cutoff_input_widget,
                                        self.select_cutoff_units_widget),
                                 self.order_input_widget,
                                 self.calculate_button,
                                 self.text_hint,
                                 self.plot_pane,
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

    def calculate_filter(self, event):
        cutoff = self.cutoff_input_widget.value *\
                 gv.frequency_units_dict[self.select_cutoff_units_widget.value]
        self.filter_obj = route_filter_class(type_str=self.select_type_widget.value,
                                             cutoff=cutoff,
                                             order=self.order_input_widget.value,
                                             gain=1)
        self.text_hint.value = str(self.filter_obj.gain_response(1j))

        scale = gv.frequency_units_dict[self.select_cutoff_units_widget.value]
        n_points = max(int(100 * scale), 1000) #Ensure a min of points
        n_points = min(n_points, int(100 * 1e3))
        end_point = complex(0, cutoff * scale * 10)
        init_point = complex(0, 0.010)
        values_x = np.geomspace(init_point, end_point, n_points)
        norm_values_x = values_x / cutoff

        values_y = self.filter_obj.gain_response(norm_values_x)

        curve = hv.Curve((norm_values_x.imag, values_y),
                         'f/fc',
                         'Gain').opts(width=500, height=300, title='Bode Plot', logx=True, show_grid=True)
        vertical_line_cutoff = hv.VLine(x= 1).opts(line_dash='dashed', line_color='red')

        self.plot_pane.object = curve * vertical_line_cutoff


