# utils.py
import pandas as pd
import google.generativeai as genai
from dotenv import load_dotenv

import os

load_dotenv()
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))



# Configuration des paramètres de sécurité
safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

def summary(input_text):
    """
    Génère un résumé structuré pour le texte donné en utilisant le modèle d'IA de Google.
    
    Args:
        input_text (str): Texte à résumer.
        
    Returns:
        str: Résumé généré structuré avec sections.
    """
    try:
        # Initialiser le modèle génératif
        model = genai.GenerativeModel(model_name="gemini-pro")
        
        # Instructions du prompt
        prompt = """
        Vous êtes un assistant d'intelligence artificielle spécialisé dans la synthèse de documents et de dialogues.
        Vous devez fournir un résumé structuré et détaillé des réunions.
        Veuillez fournir un résumé avec les sections suivantes:
        
        **Résumé**
        Fournir un résumé concis du dialogue.
        
        **Liste de présence**
        Lister tous les intervenants et leur rôle.
        
        **Points clés**
        Énumérer les points clés discutés pendant la réunion.
        
        Voici le texte de la réunion à résumer:
        """
        
        # Créer le prompt en combinant les instructions avec le texte d'entrée
        prompt_text = prompt + "\n\n" + input_text
        
        # Générer la réponse en utilisant le modèle
        response = model.generate_content(prompt_text, safety_settings=safety_settings)
        
        # Retourner le texte du résumé structuré
        return response.text.strip()
    except Exception as e:
        return f"An error occurred: {e}"


def summary_global(meeting_texts):
    """
    Génère un résumé global structuré pour toutes les réunions en prenant en compte la liste de présence et les points clés.
    
    Args:
        meeting_texts (list): Liste de textes de réunions à résumer.
        
    Returns:
        str: Résumé global généré avec sections pour la liste de présence et les points clés.
    """
    try:
        # Initialiser le modèle génératif
        model = genai.GenerativeModel(model_name="gemini-pro")
        
        # Instructions du prompt
        prompt = """
        Vous êtes un assistant d'intelligence artificielle spécialisé dans la synthèse de documents et de réunions.
        Vous devez fournir un résumé global structuré de toutes les réunions en prenant en compte les listes de présence et les points clés.
        
        **Liste de présence**
        Lister tous les intervenants et leur rôle pour chaque réunion.
        
        **Points clés**
        Énumérer les points clés discutés pendant toutes les réunions.
        
        Voici les réunions à résumer :
        """
        
        # Créer le prompt en combinant les instructions avec les textes de réunions
        prompt_text = prompt + "\n\n" + "\n\n".join(meeting_texts)
        
        # Générer la réponse en utilisant le modèle
        response = model.generate_content(prompt_text, safety_settings=safety_settings)
        
        # Retourner le texte du résumé global structuré
        return response.text.strip()
    except Exception as e:
        return f"An error occurred: {e}"


def data(file):
    df = pd.read_excel(file)
    transcripts = df['full_transcript'].dropna().tolist()
    references = df['recording_transcript'].dropna().tolist()
    data = {'Transcripts': transcripts, 'Références': references}
    df_filtered = pd.DataFrame(data)
    return df_filtered

# def summary(input_text):
#     model = genai.GenerativeModel(model_name="gemini-pro")
#     example_instructions = """
#     Vous êtes un assistant d'intelligence artificielle spécialisé dans la synthèse de documents et de dialogues.
#     Vous êtes conçu pour fournir des résumés complets, mettant en évidence les points clés.
#     Veuillez fournir un résumé du dialogue suivant :
#     """
#     prompt_parts = [example_instructions, input_text]
#     response = model.generate_content(prompt_parts)
#     return response.text
# class SummarisationListCreate(generics.ListCreateAPIView):
#     queryset = Summarisation.objects.all()
#     serializer_class = SummarisationForm

#     def perform_create(self, serializer):
#         # Debug: Print the received data
#         print("Received data:", self.request.data)

#         base64_file_data = self.request.data.get('file')
#         file_name = self.request.data.get('file_name')  # Assurez-vous que le nom du fichier est fourni

#         # Debug: Print the extracted file data and file name
#         print("Base64 file data:", base64_file_data)
#         print("File name:", file_name)

#         if not base64_file_data or not file_name:
#             raise ValidationError("File data or file name is missing.")

#         try:
#             # Décoder le fichier base64 en octets
#             file_bytes = base64_to_bytes(base64_file_data)

#             # Convertir les octets en fichier Excel
#             excel_file = bytes_to_excel_file(file_bytes, file_name)

#             # Sauvegarder l'instance avec le fichier Excel
#             instance = serializer.save(file=excel_file)

#             # Utiliser la fonction data() pour traiter le fichier Excel
#             df_filtered = data(instance.file)

#             # Debug: print the columns of the filtered dataframe
#             print(f"Columns in the filtered dataframe: {df_filtered.columns.tolist()}")

#             if 'Transcripts' not in df_filtered.columns:
#                 raise ValidationError("The processed Excel file does not contain a 'Transcripts' column.")
            
#             input_text = df_filtered['Transcripts'][0]  # Adjust the index as needed
#             summary_text = summary(input_text)
            
#             # Save the summary to the instance
#             instance.summarisation = summary_text
#             instance.save()
#         except Exception as e:
#             instance.delete()  # Optionally delete the instance if there was an error
#             raise ValidationError(f"An error occurred while processing the file: {str(e)}")
