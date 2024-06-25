import streamlit as st
import pandas as pd
from utils import summary  # Assurez-vous que cette importation fonctionne
import base64

def data(file):
    df = pd.read_excel(file)
    transcripts = df['full_transcript'].dropna().tolist()
    references = df['recording_transcript'].dropna().tolist()
    data = {'Transcripts': transcripts, 'Références': references}
    df_filtered = pd.DataFrame(data)
    return df_filtered

def get_image_as_base64(file_path):
    with open(file_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def main():
    # Convertir l'image en base64
    img_base64 = get_image_as_base64("Capture.png")

    # Affiche le logo et le titre avec couleur et animation
    st.markdown(f"""
        <div style='text-align: center;'>
            <img src='data:image/png;base64,{img_base64}' style='width: 100px;'>
            <h1 style='color: #4CAF50; animation: color-change 3s infinite;'>
                MeetSynth (Dialogue Summarization)
            </h1>
        </div>
        <style>
            @keyframes color-change {{
                0% {{ color: #4CAF50; }}
                50% {{ color: #FF6347; }}
                100% {{ color: #4CAF50; }}
            }}
        </style>
    """, unsafe_allow_html=True)

    st.write("""
      **Bienvenue dans MeetSynth !** 
    Cette application est conçue pour vous aider à générer des résumés automatiques de vos réunions. 
    Vous pouvez importer un fichier Excel contenant les transcripts complets des dialogues , 
    et obtenir un résumé concis de la réunion""")

     
    
    uploaded_file = st.file_uploader("Choisir un fichier Excel", type=["xlsx"])
    
    if uploaded_file is not None:
        try:
            df_filtered = data(uploaded_file)
            if df_filtered.empty:
                st.error("Le fichier importé ne contient pas de données valides.")
            else:
                st.write("Contenu du fichier filtré :")
                st.dataframe(df_filtered)

                if st.button("Générer le résumé"):
                    try:
                        input_text = df_filtered['Transcripts'][0] 
                        summary_result = summary(input_text)
                        st.write("Résumé du dialogue :")
                        st.write(summary_result)
                    except Exception as e:
                        st.error(f"Erreur lors de la génération du résumé : {e}")

        except Exception as e:
            st.error(f"Erreur lors de la lecture du fichier : {e}")

if __name__ == "__main__":
    main()
