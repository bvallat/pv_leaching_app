import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

#image = r'path'


def app():

    #Title
    st.title('Perovskite leaching tool')

    #####################################

    # Create a form
    st.header('User input')
    with st.form(key='pannel form'):
        st.subheader('Lead content in panel')
        input_pv_surface = float(st.number_input(label='PV surface [m2]', value = 10))
        input__pb_concentration = float(st.number_input(label='Pb concentration [g/m2]',value=0.9))
        input_prcent_leached = float(st.number_input(label='Pb leaching ratio [0-100]',value=100))
        st.write("---") 
        #---------------------------------
        st.subheader('Volume/mass of soil considered')
        input_distance_around_pv = float(st.number_input(label='Max Pb spreading distance around PV [m]',value=0.5))
        input_soil_depth = float(st.number_input(label='Max soil depth [m]',value=0.5))
        input_soil_density = float(st.number_input(label='Soil density [kg/m3]',value=3000))
        input_sorbtion_ratio = float(st.number_input(label='Soil sorption ratio [0-100]',value=100))
        submit_button = st.form_submit_button(label='Compute')


    if submit_button:
        #Create lsit for several spreading distance
        var_spreading_distances = [input_distance_around_pv*0.25,input_distance_around_pv*0.5,input_distance_around_pv*0.75,input_distance_around_pv*1,
                               input_distance_around_pv*1.25,input_distance_around_pv*1.5,input_distance_around_pv*1.75,input_distance_around_pv*2]  # distances en mètres


    #Compute all the necessary variables
        var_total_pb = input_pv_surface * input__pb_concentration * (input_prcent_leached/100)
        var_sorbed_pb = var_total_pb * (input_sorbtion_ratio/100)
        var_sorbed_pb = [var_sorbed_pb] * 8
        var_surfaces_around_PV = [x + (input_pv_surface**0.5) for x in var_spreading_distances]
        var_surfaces_around_PV = [x**2 for x in var_surfaces_around_PV]
        var_volumes_around_PV = [x * input_soil_depth for x in var_surfaces_around_PV]
        var_soil_mass_around_pv = [x * input_soil_density for x in var_volumes_around_PV]
        #var_concentrations_per_vol = (var_sorbed_pb / var_volumes_around_PV )*input_sorbtion_ratio
        var_concentrations_per_mass = [x / y for x, y in zip(var_sorbed_pb, var_soil_mass_around_pv)]
        var_concentrations_per_mass = [x * 1000 for x in var_concentrations_per_mass] #convert g/kg to mg/kg


        #Print Results
        st.header(f'Results :')

        # Create dictonary with results
        data = {
            'Total Pb in panels': [f"{round(var_total_pb,3)} g"],
            'Total Pb sorbed in soil': [f"{round(var_sorbed_pb[0],3)} g"],
            'Soil volume around PV': [f"{round(var_volumes_around_PV[3],3)} m3"],
            'Soil mass around PV': [f"{round(var_soil_mass_around_pv[3],3)} kg"],
            'Pb mass concentration in soil': [f"{round(var_concentrations_per_mass[3],3)} mg/kg"]
        }

        # Convert the dictionary in dataframe 
        df = pd.DataFrame(data)
        # Print the DataFrame dans Streamlit
        st.table(df)

        st.write("---")

        # Create a plot
        plt.figure(figsize=(10, 6))
        plt.plot(var_spreading_distances, var_concentrations_per_mass, marker='o')
        plt.title('Pb concentration in fonction of spreading distance with ' + str(input_soil_depth) + ' m depth')
        plt.xlabel('Spreading distance (m)')
        plt.ylabel('Pb concentration (mg/kg)')
        recommended_value = 83
        foen_value = 300
        #plt.axhline(y=recommended_value, color='y', linestyle='--', label=f'SCAHT recommended value')
        #plt.axhline(y=foen_value, color='r', linestyle='--', label=f'FOEN max limit')
        plt.grid(True)
        plt.show()

        st.pyplot(plt)

        st.write(f'SCAHT recommended  max value : 83mg/kg')
        st.write(f'FOEN recommended  max value : 300mg/kg')
        st.write(f'FOEN threshold for remediation : 1000mg/kg')


if __name__ == "__main__":
    app()
