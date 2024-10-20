# HairTransfer

HairTransfer is a Python application that uses computer vision; image processing and deep learning to transfer hairstyles from a face (a source image) to another (a target image).

Deep learning is applied to recognize face shapes, which is then used to filter user hairstyle feeds to only display faces with similar face shapes to ensure high quality Hair Transfer.

Implicitly, hair transfer uses face swapping but a modest attempt is made here to emphasize on hair features of the target image.


TensorFlow was used for deep learning. The Inception V3 deep learning model was retrained to recognize five face shapes.

<p align="center">
  <img src="file_storage/general/source_image.jpeg" width="30%" />
  <img src="file_storage/general/target_image.jpeg" width="30%" />
  <img src="file_storage/general/output_image.jpeg" width="30%" />
</p>


Credits: [Switching Eds with Python](https://matthewearl.github.io/2015/07/28/switching-eds-with-python/)
