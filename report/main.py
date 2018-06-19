import gas_turbine_cycle.templates
from gas_turbine_cycle.core.turbine_lib import Turbine, Atmosphere, Load, Compressor, CombustionChamber, Inlet, \
    Outlet, Source, Sink
import turbine.templates as turb_templ
import compressor.templates as comp_templ
from jinja2 import Environment, select_autoescape, FileSystemLoader
import os
import config
from compressor.average_streamline.compressor import Compressor as CompAvLine
from turbine.cooling.film_defl import FilmBladeCoolingResults
from turbine.profiling.stage import ProfilingResultsForCooling
from turbine.average_streamline.turbine import Turbine as TurbAvLine
import pickle
import comb_chamber.templates as comb_templ
from comb_chamber.geom import CombustionChamberGeom


def get_turbine(fname) -> TurbAvLine:
    file = open(fname, 'rb')
    res = pickle.load(file)['turbine']
    file.close()
    return res


def get_comb_chamber_geom(fname) -> CombustionChamberGeom:
    with open(fname, 'rb') as f:
        res = pickle.load(f)
    return res


def get_compressor(fname) -> CompAvLine:
    with open(fname, 'rb') as f:
        res = pickle.load(f)[0]
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


root_dir = os.path.dirname(os.path.dirname(__file__))

if __name__ == '__main__':
    loader = FileSystemLoader(
        [
            gas_turbine_cycle.templates.__path__[0], os.getcwd(),
            turb_templ.__path__[0],
            comp_templ.__path__[0],
            comb_templ.__path__[0],
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

    comp_avline = get_compressor(os.path.join(root_dir, config.output_dirname, 'compressor.comp'))
    comp_turb_avline = get_turbine(os.path.join(root_dir, config.output_dirname, 'comp_turbine_ave_line.avl'))
    comp_turb_st1_params = load(os.path.join(root_dir, config.output_dirname, 'comp_turb_st1_flow_params'))
    comp_turb_st2_params = load(os.path.join(root_dir, config.output_dirname, 'comp_turb_st2_flow_params'))
    power_turb_avline = get_turbine(os.path.join(root_dir, config.output_dirname, 'power_turbine_ave_line.avl'))
    comb_chamber_geom = get_comb_chamber_geom(os.path.join(root_dir, config.output_dirname, 'comb_chamber_geom.cchg'))
    cool_results = get_cooling_results(os.path.join(root_dir, config.output_dirname, 'cool_results'))
    prof_res_for_cool = get_profiling_results(os.path.join(root_dir, config.output_dirname,
                                                           'comp_turb_st1_prof_for_cool.prof'))
    hot_sector_num = 4

    with open(os.path.join(root_dir, config.output_dirname,
                           config.cycle_results), 'rb') as file:
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
        name_gas_comp=name_gas_comp,

        comp_avline=comp_avline,

        comp_turb_avline=comp_turb_avline,
        comp_turb_st1_params=comp_turb_st1_params,
        comp_turb_st2_params=comp_turb_st2_params,

        power_turb_avline=power_turb_avline,

        comb_geom=comb_chamber_geom,

        cool_film_params=cool_results.film_params[hot_sector_num],
        cool_local_params=cool_results.local_params[hot_sector_num],
        cool_results=cool_results,
        comp_turb_st1_sa_blade_num=prof_res_for_cool.blade_num
    )

    with open('report.tex', 'w', encoding='utf-8') as file:
        file.write(content)

    # practice_template = env.get_template('practice_report_template.tex')
    #
    # content = practice_template.render(
    #     atm=atmosphere,
    #     inlet=inlet,
    #     comp=compressor,
    #     sink=sink,
    #     comb_chamber=comb_chamber,
    #     turb_c=comp_turbine,
    #     source=source,
    #     turb_p=power_turbine,
    #     outlet=outlet,
    #     load=turb_load,
    #     N_gen=N_gen,
    #     eta_gen=eta_gen,
    #     name_gen=name_gen,
    #     N_gas_comp=N_gas_comp,
    #     mass_rate_gas_comp=mass_rate_gas_comp,
    #     press_in_gas_comp=press_in_gas_comp,
    #     press_out_gas_comp=press_out_gas_comp,
    #     T_in_gas_comp=T_in_gas_comp,
    #     T_out_gas_comp=T_out_gas_comp,
    #     rho_gas_comp=rho_gas_comp,
    #     c_p_nat_gas_av=c_p_nat_gas_av,
    #     k_nat_gas_av=k_nat_gas_av,
    #     eta_ad_gas_comp=eta_ad_gas_comp,
    #     eta_el_eng=eta_el_eng,
    #     name_gas_comp=name_gas_comp
    # )
    #
    # with open('practice_report.tex', 'w', encoding='utf-8') as file:
    #     file.write(content)