import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

image = r'scheme.png'
header = r'header.png'


def app():

    st.image(header, use_column_width=True)
    #Title
    st.title('PerPV lead leaching tool (alpha version ) ')
    st.text("""
    This application allows you to calculate the average concentration of lead (Pb) 
    that could be sorbed by the soil in the event of a lead leak from a perovskite 
    solar panel.
    
    It uses the total mass of lead contained in the system, taking into account the 
    surface area and lead density of the panel, as well as the percentage of lead 
    released as indicated by the user.
    
    The application then divides this mass of lead by a certain volume of soil, which 
    depends on the diffusion area and the depth to which the user estimates the lead 
    will leach. It takes into account the percentage of lead absorbed by the soil and 
    returns a mass concentration of lead in the soil, calculated based on these 
    parameters and the density of the soil type chosen by the user.
    
    This is a simplified model that does not take into account the dynamics of solute 
    transport
    
    Instead, it serves to provide orders of magnitude with the following assumptions:
    
    - The lead is distributed perfectly homogeneously in the considered volume of soil.
    - The lead is distributed only within the boundaries delimited by the user.
    
    Please note that this model is designed to provide a general idea of potential 
    lead concentrations and does not reflect the exact values in a real-world scenario.
    """)

    st.write("---") 

    #####################################

    # Create a form
    st.header('User input')
    with st.form(key='pannel form'):
        st.subheader('Lead content in panel')
        input_pv_surface = float(st.number_input(label='PV surface [m2]', value = 10))
        
        #Concentration
        input_user_pb_concentration = float(st.number_input(label='Pb concentration [g/m2] - max concentration is 3.000g/m2',value=0.9,format="%.3f",step=0.001, min_value=0.001, max_value=3)
        st.write("---") 

        st.text(f'If unknown, you can compute concentration from thickness and material type')
        input_thickness = st.number_input('Thickness of perovskite layer [nm] - maximum value is 1000nm',value = 200, min_value=1, max_value=1000)
        input_thickness = input_thickness*(10**-7) #convert in cm

        # Mateiral list and value
        material_dict = {
            'MAPbI3 (1.36 gPb/cm3)': 1.37,
            'FAPbI3 (1.26 gPb/cm3)': 1.26, 
            'CsPbI3 (1.15 gPb/cm3)': 1.15
        }
        input_list_materials = ['MAPbI3 (1.36 gPb/cm3)','FAPbI3 (1.26 gPb/cm3)', 'CsPbI3 (1.15 gPb/cm3)']
        input_material = st.selectbox('Material', input_list_materials)

        submit_button_concentration = st.form_submit_button(label='Get concentration')

        if submit_button_concentration :
            input_pb_concentration_mat = input_thickness*material_dict[input_material]*100*100
            st.text(f'Calculated pb concentration is : ' + str(round(input_pb_concentration_mat,2))+' g/m2')
            st.text(f" ! Don't forget to copy it the in Pb concentration !")

        st.write("---") 

        input_pb_concentration = input_user_pb_concentration
        
        input_prcent_leached = float(st.number_input(label='Pb leaching ratio [0-100]',value=100))
        st.write("---") 
        #---------------------------------
        st.subheader('Volume/mass of soil considered')
        st.image(image,use_column_width=True)
        input_distance_around_pv = float(st.number_input(label='Max Pb spreading distance around PV (d) [m]',value=0.5))
        input_soil_depth = float(st.number_input(label='Max soil depth (z) [m]',value=0.2))
        input_checkbox_surface_bellow_pv = st.checkbox(label = "Include volume bellow PV")

        #Density
        input_soil_density = float(st.number_input(label='Soil density [kg/m3]',value=1408))
        st.text(f"If needed, bellow are shown typical soils densities (average is 1408 kg/m3)")
        
        soil_data = {
        "Sand": 1430,
        "Loamy Sand": 1460,
        "Sandy Loam": 1460,
        "Loam": 1430,
        "Silty Loam": 1380,
        "Silt": 1380,
        "Sandy Clayey Loam": 1500,
        "Clayey Loam": 1390,
        "Silty Clayey Loam": 1300,
        "Silty Clay": 1260,
        "Sandy Clay": 1470,
        "Clay": 1330
        }

        soil_data_sorted = dict(sorted(soil_data.items(), key=lambda item: item[1], reverse=True))

        # Convert in DataFrame
        df_sorted = pd.DataFrame(list(soil_data_sorted.items()), columns=['Soil Type', 'Density (kg/m3)'])
        
        # chnage the format to avoid the comma for thousands
        df_sorted['Density (kg/m3)'] = df_sorted['Density (kg/m3)'].apply(lambda x: '{0:.0f}'.format(x))
        
        # Display DataFrame in Streamlit
        st.dataframe(df_sorted)




        
        input_sorbtion_ratio = float(st.number_input(label='Soil sorption ratio [0-100]',value=100))
        submit_button = st.form_submit_button(label='Compute')


    if submit_button:
        #Create lsit for several spreading distance
        var_spreading_distances = [input_distance_around_pv*0.25,input_distance_around_pv*0.5,input_distance_around_pv*0.75,input_distance_around_pv*1,
                               input_distance_around_pv*1.25,input_distance_around_pv*1.5,input_distance_around_pv*1.75,input_distance_around_pv*2]  # distances en mètres


    #Compute all the necessary variables
        var_total_pb = input_pv_surface * input_pb_concentration * (input_prcent_leached/100)
        var_sorbed_pb = var_total_pb * (input_sorbtion_ratio/100)
        var_sorbed_pb = [var_sorbed_pb] * 8
        var_surfaces_around_PV = [x + (input_pv_surface**0.5) for x in var_spreading_distances]
        var_surfaces_around_PV = [x**2 for x in var_surfaces_around_PV]
        var_surfaces_around_PV = [x - input_pv_surface for x in var_surfaces_around_PV]
        if input_checkbox_surface_bellow_pv == True :
            var_surfaces_around_PV = [x + input_pv_surface for x in var_surfaces_around_PV]
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
        plt.title('Increase in Pb concentration in soil in fonction of spreading distance with ' + str(input_soil_depth) + ' m depth')
        plt.xlabel('Spreading distance (m)')
        plt.ylabel('Increase in Pb concentration in soil (mg/kg)')
        recommended_value = 83
        foen_value = 300
        plt.axhline(y=recommended_value, color='y', linestyle='--', label=f'SCAHT recommended value')
        #plt.axhline(y=foen_value, color='r', linestyle='--', label=f'FOEN max limit')
        plt.grid(True)
        plt.show()

        st.pyplot(plt)

        st.write(f'SCAHT recommended  max value : 83mg/kg')
        st.write(f'FOEN recommended  max value : 300mg/kg')
        st.write(f'FOEN threshold for remediation : 1000mg/kg')


if __name__ == "__main__":
    app()
