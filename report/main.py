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
        results = pickle.load(file)

    units = results[0]
    gen_par = results[1]
    gas_comp_par = results[2]
    atmosphere = units['atmosphere']
    inlet = units['inlet']
    comp_turbine = units['comp_turbine']
    outlet = units['outlet']
    turb_load = units['turb_load']
    zero_load1 = units['zero_load1']
    zero_load2 = units['zero_load2']
    power_turbine = units['power_turbine']
    compressor = units['compressor']
    sink = units['sink']
    source = units['source']
    comb_chamber = units['comb_chamber']

    N_gen = gen_par['N_gen']
    eta_gen = gen_par['eta_gen']
    name_gen = gen_par['name_gen']

    N_gas_comp = gas_comp_par['N_gas_comp']
    mass_rate_gas_comp = gas_comp_par['mass_rate_gas_comp']
    press_in_gas_comp = gas_comp_par['press_in_gas_comp']
    press_out_gas_comp = gas_comp_par['press_out_gas_comp']
    T_in_gas_comp = gas_comp_par['T_in_gas_comp']
    T_out_gas_comp = gas_comp_par['T_out_gas_comp']
    rho_gas_comp = gas_comp_par['rho_gas_comp']
    c_p_nat_gas_av = gas_comp_par['c_p_nat_gas_av']
    k_nat_gas_av = gas_comp_par['k_nat_gas_av']
    eta_ad_gas_comp = gas_comp_par['eta_ad_gas_comp']
    eta_el_eng = gas_comp_par['eta_el_eng']
    name_gas_comp = gas_comp_par['name_gas_comp']

    N_e_specific = turb_load.consumable_labour
    G_comp = turb_load.power / N_e_specific

    dip_template = env.get_template('report_template.tex')

    content = dip_template.render(
        atm=atmosphere,
        inlet=inlet,
        comp=compressor,
        sink=sink,
        comb_chamber=comb_chamber,
        turb_c=comp_turbine,
        source=source,
        turb_p=power_turbine,
        outlet=outlet,
        load=turb_load,
        N_gen=N_gen,
        eta_gen=eta_gen,
        name_gen=name_gen,
        N_gas_comp=N_gas_comp,
        mass_rate_gas_comp=mass_rate_gas_comp,
        press_in_gas_comp=press_in_gas_comp,
        press_out_gas_comp=press_out_gas_comp,
        T_in_gas_comp=T_in_gas_comp,
        T_out_gas_comp=T_out_gas_comp,
        rho_gas_comp=rho_gas_comp,
        c_p_nat_gas_av=c_p_nat_gas_av,
        k_nat_gas_av=k_nat_gas_av,
        eta_ad_gas_comp=eta_ad_gas_comp,
        eta_el_eng=eta_el_eng,
        name_gas_comp=name_gas_comp
    )

    with open('report.tex', 'w', encoding='utf-8') as file:
        file.write(content)

    practice_template = env.get_template('practice_report_template.tex')

    content = practice_template.render(
        atm=atmosphere,
        inlet=inlet,
        comp=compressor,
        sink=sink,
        comb_chamber=comb_chamber,
        turb_c=comp_turbine,
        source=source,
        turb_p=power_turbine,
        outlet=outlet,
        load=turb_load,
        N_gen=N_gen,
        eta_gen=eta_gen,
        name_gen=name_gen,
        N_gas_comp=N_gas_comp,
        mass_rate_gas_comp=mass_rate_gas_comp,
        press_in_gas_comp=press_in_gas_comp,
        press_out_gas_comp=press_out_gas_comp,
        T_in_gas_comp=T_in_gas_comp,
        T_out_gas_comp=T_out_gas_comp,
        rho_gas_comp=rho_gas_comp,
        c_p_nat_gas_av=c_p_nat_gas_av,
        k_nat_gas_av=k_nat_gas_av,
        eta_ad_gas_comp=eta_ad_gas_comp,
        eta_el_eng=eta_el_eng,
        name_gas_comp=name_gas_comp
    )

    with open('practice_report.tex', 'w', encoding='utf-8') as file:
        file.write(content)