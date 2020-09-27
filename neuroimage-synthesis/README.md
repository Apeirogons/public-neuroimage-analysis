A image conversion model converting a (more commonly acquired) T1 neuroimage into a (less commonly acquired) FA neuroimage.
This has implications for synthesis of unavailable data in a research setting.


Data obtained from the CamCAN dataset at:
https://camcan-archive.mrc-cbu.cam.ac.uk/dataaccess/ 

Keep in mind that due to resource limitations, batch size is set to 1. The generation algorithm takes an autoencoder-compressed representation of the T1 image and outputs an autoencoder-compressed representation of the FA image, which may be decoded into a 'realistic' image.
