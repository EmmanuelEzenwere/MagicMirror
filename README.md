# HairTransfer

HairTransfer is a Python application that uses computer vision; image processing and deep learning to transfer hairstyles from a face (a source image) to another (a target image).

Deep learning is applied to recognize face shapes, which is then used to filter user hairstyle feeds to only display faces with similar face shapes to ensure high quality Hair Transfer.

Implicitly, hair transfer uses face swapping but a modest attempt is made here to emphasize on hair features of the target image.


TensorFlow was used for deep learning. The Inception V3 deep learning model was retrained to recognize five face shapes.

<div style="display: flex; justify-content: center; gap: 10px;">
    <img src="file_storage/trash/temp_files/WhatsApp Image 2024-10-20 at 01.03.35-2.jpeg" style="width: auto; height: 100%;">
    <img src="file_storage/hairstyles/female/WhatsApp Image 2024-10-20 at 01.03.35-2.jpeg" style="width: auto; height: 100%;">
    <img src="file_storage/hairstyles/female/WhatsApp Image 2024-10-20 at 01.03.35-2.jpeg" style="width: auto; height: 100%;">
</div>


Credits: [Switching Eds with Python](https://matthewearl.github.io/2015/07/28/switching-eds-with-python/)
