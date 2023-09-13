import pyvips


def convert_to_dzi(input_file, output_file):
    """
    Convert a .tif or .mrxs file to .dzi format using VIPS.

    Args:
    - input_file (str): Path to the input .tif or .mrxs file.
    - output_file_without_extension (str): Desired path to the output .dzi file without the extension.

    Returns:
    - str: Path to the generated .dzi file.
    """

    # Load the image
    image = pyvips.Image.new_from_file(input_file, access='sequential')

    # Save the image to dzi format
    image.dzsave(output_file)

    return f"{output_file}"
