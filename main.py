import streamlit as st
from mel import Mel

st.set_page_config(page_title="Spectogram Generator", page_icon=":📈:", layout="wide")
st.title("📈 Spectogram Generator")

uploaded_file = st.file_uploader("Drop Audio file for which you would like to view spectrogram for:", type=['wav', 'mp3'],)

def get_user_settings():
    x_res = st.sidebar.slider("x_res", min_value=64, max_value=2048, value=256, step=64, help="Increases Time on the ploted image")
    y_res = st.sidebar.slider("y_res", min_value=64, max_value=2048, value=256, step=64, help="Increases Bins of the Spectogram")
    show_advanced_settings = st.sidebar.checkbox("Show remaining settings")
    if show_advanced_settings:
        sample_rate = st.sidebar.slider("Sample Rate", min_value=4096, max_value=22050, value=22050, step=1)
        n_fft = st.sidebar.slider("n_fft", min_value=64, max_value=4096, value=2048, step=64)
        hop_length = st.sidebar.slider("hop_length", min_value=32, max_value=1024, value=512, step=32)
        top_db = st.sidebar.slider("top_db", min_value=0, max_value=100, value=80, step=1)
        n_iter = st.sidebar.slider("n_iter", min_value=1, max_value=100, value=32, step=1)
        column_width = st.sidebar.checkbox("Column Width",help="Image width don't exceed page width", value=True)
    else:
        sample_rate, n_fft, hop_length, top_db, n_iter, column_width = None, None, None, None, None, True
    return x_res, y_res, sample_rate, n_fft, hop_length, top_db, n_iter, column_width

if uploaded_file is not None:
    mel = Mel()
    bytes_data = uploaded_file
    mel.load_audio(audio_file=uploaded_file)

    x_res, y_res, sample_rate, n_fft, hop_length, top_db, n_iter, column_width = get_user_settings()
    mel.set_resolution(x_res, y_res)

    num_slices = mel.get_number_of_slices()
    slice_number = st.slider("Select Slice", min_value=0, max_value=num_slices - 1, value=0, step=1)

    image = mel.audio_slice_to_image(slice_number)
    audio = mel.get_audio_slice(slice_number)
    if image:
        st.image(image, caption=f"Spectrogram for Slice {slice_number}", use_column_width='auto' if column_width else False)
        st.audio(audio, sample_rate=mel.get_sample_rate())


st.sidebar.title("About")
st.sidebar.info("This is a Streamlit application to generate spectrograms from audio files using Mel spectrogram technique.")
