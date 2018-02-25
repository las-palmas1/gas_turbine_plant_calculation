import gas_turbine_cycle.templates
from gas_turbine_cycle.core.turbine_lib import Turbine, Atmosphere, Load, Compressor, CombustionChamber, Inlet, \
    Outlet, Source, Sink
import turbine.templates as turb_templ
from jinja2 import Environment, select_autoescape, FileSystemLoader
import os
from turbine.cooling.film_defl import FilmBladeCoolingResults
from turbine.profiling.stage import ProfilingResultsForCooling
from turbine.average_streamline.turbine import Turbine
import pickle


def get_turbine(fname) -> Turbine:
    file = open(fname, 'rb')
    res = pickle.load(file)
    file.close()
    return res


def get_cooling_results(fname) -> FilmBladeCoolingResults:
    file = open(fname, 'rb')
    res = pickle.load(file)
    file.close()
    return res


def get_profiling_results(fname) -> ProfilingResultsForCooling:
    file = open(fname, 'rb')
    res = pickle.load(file)
    file.close()
    return res


def load(fname):
    file = open(fname, 'rb')
    res = pickle.load(file)
    file.close()
    return res


if __name__ == '__main__':
    loader = FileSystemLoader(
        [
            gas_turbine_cycle.templates.__path__[0], os.getcwd(),
            turb_templ.__path__[0],
            os.getcwd()
        ]
    )

    env = Environment(
        loader=loader,
        autoescape=select_autoescape(['tex']),
        block_start_string='</',
        block_end_string='/>',
        variable_start_string='<<',
        variable_end_string='>>',
        comment_start_string='<#',
        comment_end_string='#>'
    )

    with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output results/cycle.cyc'), 'rb') as file:
        unit_arr = pickle.load(file)

    atmosphere = unit_arr[0]
    inlet = unit_arr[1]
    comp_turbine = unit_arr[2]
    outlet = unit_arr[3]
    turb_load = unit_arr[4]
    zero_load1 = unit_arr[5]
    zero_load2 = unit_arr[6]
    power_turbine = unit_arr[7]
    compressor = unit_arr[8]
    sink = unit_arr[9]
    source1 = unit_arr[10]
    source2 = unit_arr[11]
    comb_chamber = unit_arr[12]

    N_e_specific = turb_load.consumable_labour * power_turbine.g_in
    G_comp = turb_load.power / N_e_specific

    template = env.get_template('report_template.tex')

    content = template.render(
        atm=atmosphere,
        inlet=inlet,
        comp=compressor,
        sink=sink,
        comb_chamber=comb_chamber,
        source1=source1,
        turb_c=comp_turbine,
        source2=source2,
        turb_p=power_turbine,
        outlet=outlet,
        load=turb_load,
    )

    with open('report.tex', 'w', encoding='utf-8') as file:
        file.write(content)