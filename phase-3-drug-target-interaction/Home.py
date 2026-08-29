from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from utils.page_helpers import *

title()
project_introduction = st.container()
about_us = st.container()

with project_introduction:
    st.subheader("Introduction")
    st.markdown("""
            The project focused on the interactions between chemical compounds and biological proteins within the human body, known as drug-target interactions (DTIs), which are pivotal in the realms of drug discovery and pharmacology. Experimentally identifying these interactions is often slow and constrained by financial resources and the challenges associated with protein purification.

            The occurrence of unintended or unforeseen DTIs can lead to significant adverse effects. Thus, the development of computational machine learning models capable of rapidly and accurately predicting the binding affinity between thousands of drugs and proteins could significantly benefit medicinal chemistry and drug development, serving as a complementary tool to biological experimentation.

            """)
    st.markdown("""
                **Initial Goals**: The objective was to compile a comprehensive dataset from publicly accessible sources on known DTIs, creating a newly curated collection. Utilizing this dataset, the plan was to develop and train various machine learning models employing basic QSAR descriptors based on the chemical attributes of drugs and the sequence and 3D structural data of proteins, obtained from [AlphaFold](https://alphafold.ebi.ac.uk/), to ascertain their binding potential.

            """)
    st.markdown("""
            **Actual Achievements**: A dataset of 163,080 DTIs was gathered using a variety of databases, 
            libraries and biochemical APIs, subsets of which were used to train classification 
            models, evaluated using dummy models, holdout test sets and model interpretability tools. 
            Classification models would try to predict whether a drug-protein pair would
            bind together or not.
            """)

# with about_us:
#     st.subheader("About")
#     st.markdown("""
#                 - Created by George Iniatis as part of a 5th year computer science project at the University of Glasgow
#                 - Supervised by [Dr. Jake Lever](https://www.gla.ac.uk/schools/computing/staff/jakelever/)
#                 """)
#     st.subheader("Useful Links")
#     st.markdown("""
#                 - [Dissertation](https://drive.google.com/file/d/1PxtbJ2dam5OzJq-qUniG39A37cO22_3X/view?usp=share_link)
#                 - [GitHub Page](https://github.com/GeorgeIniatis/AlphaFold_Dataset_Drug_Binding_Prediction) 
#                 - [GitHub Wiki](https://github.com/GeorgeIniatis/AlphaFold_Dataset_Drug_Binding_Prediction/wiki) 
#                 - [Google Drive](https://drive.google.com/drive/folders/1VjRcpX_pHmt70I8neKLktm2N8S_dSptj?usp=share_link) - Holding all the trained models, datasets and embeddings
#                 """)