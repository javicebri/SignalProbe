import panel as pn
import holoviews as hv
from bokeh.models import GlyphRenderer, LinearAxis, LinearScale, Range1d

import pandas as pd
import numpy as np
import GLOBAL_VARS as gv

from model.filter import Filter, Butterwoth, route_filter_class
from controller.setActions import plot_secondary

hv.extension('bokeh')
pn.extension()

class FilterTab:
    def __init__(self):
        self.ad = None # Analog or Digital
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

        self.normalize_radio_button_group = pn.widgets.RadioButtonGroup(options=gv.normalize_options,
                                                                        value=gv.normalize_options[0],
                                                                        name='Normalize',
                                                                        visible=False)

        # Text widgets
        self.text_hint = pn.widgets.StaticText(name='Hint', value='')
        self.text_f0_gain_value = pn.widgets.StaticText(name='Gain f0', value='', visible=False)
        self.text_fc_gain_value = pn.widgets.StaticText(name='Gain fc', value='', visible=False)
        self.text_fc_phase_value = pn.widgets.StaticText(name='Phase fc', value='', visible=False)
        self.text_hint.value = "Select A/D and type of filter."

        # Input widgets
        self.cutoff_input_widget = pn.widgets.FloatInput(name='Cutoff frequency',
                                                         value=1.0,
                                                         start=0.1,
                                                         visible=True,
                                                         width=100)
        self.order_input_widget = pn.widgets.IntInput(name='Order',
                                                      value=1,
                                                      start=1,
                                                      visible=True,
                                                      width=100)

        # # Checkbox widgets
        # self.seed_checkbox = pn.widgets.Checkbox(name='As random seed', visible=False, align='end')

        # Button widgets
        self.calculate_button = pn.widgets.Button(name="Calculate", button_type="primary", visible=True)
        self.calculate_button.on_click(self.calculate_filter)
        self.text_hint.value = ''
        # Vars
        self.content = pn.Row(
            pn.Column(self.select_ad_widget,
                      self.select_type_widget,
                      pn.Row(self.cutoff_input_widget,
                             self.select_cutoff_units_widget),
                      self.order_input_widget,
                      self.calculate_button,
                      self.text_hint,
                      ),
            pn.Column(self.normalize_radio_button_group,
                      self.plot_pane,
                      self.text_f0_gain_value,
                      self.text_fc_gain_value,
                      self.text_fc_phase_value
                      ),
            width=500)

    def set_select_ad(self, event):
        """
        Selector of Analog or Digital
        :param event: scroll selector event
        :return: None
        """
        if isinstance(event, str):
            self.ad = event
            self.filter_list = gv.filter_options_dict[self.ad]
        else:
            self.ad = event.obj.value
            self.filter_list = gv.filter_options_dict[self.ad]
            self.select_type_widget.options = self.filter_list
            self.select_type_widget.value = self.filter_list[0]

    def calculate_filter(self, event):
        """
        Calculate filter response and plot it.
        :param event: Button click event
        :return: None
        """
        cutoff = self.cutoff_input_widget.value *\
                 gv.frequency_units_dict[self.select_cutoff_units_widget.value]
        self.filter_obj = route_filter_class(type_str=self.select_type_widget.value,
                                             cutoff=cutoff,
                                             order=self.order_input_widget.value,
                                             gain=1)
        self.text_f0_gain_value.visible = True
        self.text_fc_gain_value.visible = True
        self.text_fc_phase_value.visible = True
        self.normalize_radio_button_group.visible = False
        self.text_hint.value = "Done."

        scale = gv.frequency_units_dict[self.select_cutoff_units_widget.value]
        n_points = max(int(100 * scale), 1000)  # Ensure a min of points
        n_points = min(n_points, int(100 * 1e3))
        end_point = complex(0, cutoff * scale * 10)
        init_point = complex(0, 0.010)
        values_x = np.geomspace(init_point, end_point, n_points)

        if self.normalize_radio_button_group.value == "Yes":
            values_x = values_x / cutoff
            w_cutoff = 1j
        else:
            w_cutoff = 2 * np.pi * cutoff

        phase_response_0_dict = self.filter_obj.gain_phase_response(np.array([0j]))
        phase_response_cutoff_dict = self.filter_obj.gain_phase_response(np.array([w_cutoff]))
        phase_response_values_dict = self.filter_obj.gain_phase_response(values_x)

        self.text_f0_gain_value.value = str(phase_response_0_dict['Gain'][0])
        self.text_fc_gain_value.value = str(round(phase_response_cutoff_dict['Gain'][0], 3))
        self.text_fc_phase_value.value = str(phase_response_cutoff_dict['Phase'][0] * (180 / np.pi))


        gain_values = phase_response_values_dict['Gain']
        phase_values = phase_response_values_dict['Phase'] * (180 / np.pi)  # In deg

        gain_curve = hv.Curve((values_x.imag, gain_values),
                              'f/fc',
                              'Gain',
                              label='Gain').opts(tools=['hover'], width=500, height=300, title='Bode Plot',
                                           logx=True, show_grid=True)
        phase_curve = hv.Curve((values_x.imag, phase_values),
                               'f/fc',
                               'Phase [º]',
                               label='Phase').opts(tools=['hover'], width=500, height=300, logx=True, show_grid=True)
        vertical_cutoff_line = hv.VLine(x=1, label='Cutoff freq',).opts(line_dash='dashed', line_color='black')

        self.plot_pane.object = (gain_curve * phase_curve.opts(hooks=[plot_secondary]) *\
                                 vertical_cutoff_line)







