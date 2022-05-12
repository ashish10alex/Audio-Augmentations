description_dict = dict()

un_augmented_description = r"""
Un-augmented mixture was created as follows
"""

gaussian_noise_description = r"""
  One of the predominant ways to augments training examples in deep learning is to add additive Gaussian noise to 
        training examples. Gaussian noise was added to mixture  \(\boldsymbol{\bar{x}} \) as
        follows:

        \begin{equation}
        \boldsymbol{\bar{x}_{ga}} = \boldsymbol{\bar{x}} + \textit{A} \times \boldsymbol{\bar{g}}.
        \end{equation}

        Where \( \boldsymbol{\bar{x}}_{ga} \) is the Gaussian augmented mixture and \( \boldsymbol{\bar{g}} \) is gaussian noise
        sampled from normal distribution and \( A \) is the Amplitude with which Gaussian noise was added. Higher the value
        of \( A \) more noiser is  the gaussian noise. \( A \) is randomly sampled from an uniform distribution as:

        \begin{equation}
        A = \mathcal{U}(Amin, Amax).
        \end{equation}
"""

short_noise_description = r"""
Short noise augmentation
"""
time_mask_description = r"""
Time masking augmentation
"""
frequency_masking_description = r"""
Freqeuncy masking augmentation
"""
time_freqeuncy_mask_description = r"""
Time frequency masking augmentation
"""

time_stretch_description = r"""
Time stretch augmentation
"""
pitch_shift_description = r"""
Pitch shift augmentation
"""
mixup_description = r"""
Mixup augmentation
"""
cutmix_description = r"""
CutMix augmentation
"""
description_dict["Un Augmented"] = un_augmented_description
description_dict["Gaussian Noise Augmentation"] = gaussian_noise_description
description_dict["Short Noise Augmentation"] = short_noise_description
description_dict["Time Masking Augmentation"] = time_mask_description
description_dict["Frequency Masking Augmentation"] = frequency_masking_description
description_dict[
    "Time Frequency Masking Augmentation"
] = time_freqeuncy_mask_description
description_dict["Time Stretch Augmentation"] = time_stretch_description
description_dict["Pitch Shift Augmentation"] = pitch_shift_description
description_dict["Mixup Augmentation"] = mixup_description
description_dict["CutMix Augmentation"] = cutmix_description
