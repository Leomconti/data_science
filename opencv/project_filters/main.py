import streamlit as st
import numpy as np
import cv2
from PIL import Image, ImageEnhance

OUTPUT_WIDTH = 500


def main():
    st.sidebar.header("Menu")
    st.sidebar.info("Filters with opencv")
    st.sidebar.markdown("Application to apply filters in photos, using OpenCV and Streamlit")

    options_menu = ["Filters", "About"]
    selected = st.sidebar.selectbox("Select an option", options_menu)

    our_image = Image.open("project_filters/empty.jpg")

    if selected == "Filters":
        st.title("Project: Filters")
        st.text("by Leonardo Mosimann Conti")

        # carregar e exibir imagem
        # our_image = cv2.imread(file_name)  ---> Não vai dar certo
        # deve-se ler a imagem pelo streamlit, processar com opencv, e mostrar como streamlit
        st.subheader("Upload an image file")
        image_file = st.file_uploader("Select an image", type=['jpg', 'jpeg', 'png'])

        # quando alguma imagem for selecionada, utilizar essa ao inves da empty
        if image_file is not None:
            our_image = Image.open(image_file)
        st.sidebar.text("Original Image")
        st.sidebar.image(our_image, width=150)

        col1, col2 = st.columns(2)

        # filtros que podem ser aplicados
        filters = st.sidebar.radio("Filters", ['Original', 'Grayscale', 'Sketch', 'Sepia', 'Blur',
                                               'Canny', 'Contrast'])

        if filters == 'Grayscale':
            converted_image = np.array(our_image.convert('RGB'))
            gray_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2GRAY)

            col1.header("Original")
            col1.image(our_image, use_column_width=True)
            col2.header("Grayscale")
            col2.image(gray_image, use_column_width=True)
            # st.image(gray_image, width=OUTPUT_WIDTH, caption="Imagem com filtro Grayscale")

        elif filters == 'Sketch':
            converted_image = np.array(our_image.convert('RGB'))
            gray_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2GRAY)
            inv_gray_image = 255 - gray_image
            blur_image = cv2.GaussianBlur(inv_gray_image, (21, 21), 0,0)
            sketch_image = cv2.divide(gray_image, 255 - blur_image, scale=256)

            col1.header("Original")
            col1.image(our_image, use_column_width=True)
            col2.header("Sketch")
            col2.image(sketch_image, use_column_width=True)
            # st.image(sketch_image, width=OUTPUT_WIDTH, caption="Imagem com filtro Desenho")

        elif filters == 'Sepia':
            converted_image = np.array(our_image.convert('RGB'))
            converted_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2BGR)
            kernel = np.array([[0.272, 0.534, 0.131],
                               [0.349, 0.686, 0.168],
                               [0.393, 0.769, 0.189]])
            sepia_image = cv2.filter2D(converted_image, -1, kernel)

            col1.header("Original")
            col1.image(our_image, use_column_width=True)
            col2.header("Sepia")
            col2.image(sepia_image, channels="BGR", use_column_width=True)
            # st.image(sepia_image, channels="BGR", width=OUTPUT_WIDTH, caption="Imagem com filtro Sépia")

        elif filters == 'Blur':
            # step = 2, para nao parar em numeros pares, como comeca em impar sempre dara impar
            b_amount = st.sidebar.slider("Kernel (n x n)", 3, 81, 9, step=2)
            converted_image = np.array(our_image.convert('RGB'))
            converted_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2BGR)
            blur_image = cv2.GaussianBlur(converted_image, (b_amount, b_amount), 0, 0)

            col1.header("Original")
            col1.image(our_image, use_column_width=True)
            col2.header("Blur")
            col2.image(blur_image, channels="BGR", use_column_width=True)
            # st.image(blur_image, channels="BGR", width=OUTPUT_WIDTH, caption="Imagem com filtro Blur ({} x {}).".format(b_amount, b_amount))

        elif filters == 'Canny':
            converted_image = np.array(our_image.convert('RGB'))
            converted_image = cv2.cvtColor(converted_image, cv2.COLOR_RGB2BGR)
            blur_image = cv2.GaussianBlur(converted_image, (11, 11), 0)
            canny = cv2.Canny(blur_image, 100, 150)

            col1.header("Original")
            col1.image(our_image, use_column_width=True)
            col2.header("Canny Edge Detection")
            col2.image(canny, use_column_width=True)
            # st.image(canny, width=OUTPUT_WIDTH, caption="Imagem com filtro Canny")

        elif filters == "Contrast":
            c_amount = st.sidebar.slider("Constrast", 0.0, 2.0, 1.0)
            enhancer = ImageEnhance.Contrast(our_image)
            contrast_image = enhancer.enhance(c_amount)

            col1.header("Original")
            col1.image(our_image, use_column_width=True)
            col2.header("Contraste")
            col2.image(contrast_image, use_column_width=True)
            # st.image(contrast_image, width=OUTPUT_WIDTH, caption="Imagem com contraste em {}".format(c_amount))

        elif filters == 'Original':
            st.header("Original")
            st.image(our_image, width=OUTPUT_WIDTH)
        else:
            st.image(our_image, width=OUTPUT_WIDTH)

    elif selected == 'About':
        st.subheader("This is my first project using OpenCV and Streamlit. In my computer vision studies, "
                     "I found essential to understand how image manipulation works, such as filters and kernels, "
                     "and this project helped me solidify this concepts.")
        st.markdown("For more information, check out my [LinkedIn](https://linkedin.com/in/leomconti)")
        st.text("Leonardo Mosimann Conti")
        st.success("Instagram @leomconti")


if __name__ == '__main__':
    main()
