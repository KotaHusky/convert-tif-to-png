import os
import tempfile
from PIL import Image
from convert_tif_to_png.main import process_directory, process_files, ImageSize, log_message, resize_image, process_file

def test_process_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a TIF file in the temporary directory
        tif_path = os.path.join(tmpdir, 'test.tif')
        img = Image.new('RGB', (100, 100), color='red')
        img.save(tif_path)
        
        # Create an ineligible file in the temporary directory
        txt_path = os.path.join(tmpdir, 'test.txt')
        
        # Create a hidden file in the temporary directory
        hidden_path = os.path.join(tmpdir, '.test-hidden.tif')
        
        # Create a TIF file in a subdirectory
        subdir_path = os.path.join(tmpdir, 'subdir')
        os.mkdir(subdir_path)
        tif_path2 = os.path.join(subdir_path, 'test2.tif')
        img2 = Image.new('RGB', (100, 100), color='blue')
        img2.save(tif_path2)

        # Process the directory
        process_directory(tmpdir, None, ImageSize.ORIGINAL, None)

        # Check that only the TIF files at the root level were processed
        png_path = os.path.join(tmpdir, 'test.png')
        subdir_png_path = os.path.join(subdir_path, 'test2.png')
        assert os.path.exists(png_path), "PNG file does not exist"
        assert not os.path.exists(hidden_path), "Hidden file was processed"
        assert not os.path.exists(subdir_png_path), "File in subdirectory was processed"
        
def test_process_directory_with_pattern():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a TIF file in the temporary directory
        tif_path = os.path.join(tmpdir, 'mytest123.tif')
        img = Image.new('RGB', (100, 100), color='red')
        img.save(tif_path)
        
        # Create an ineligible TIFF file in the temporary directory
        tif_path2 = os.path.join(tmpdir, 'CANON12345-ENHANCED-NR.tif')
        img2 = Image.new('RGB', (100, 100), color='blue')
        img2.save(tif_path2)
        
        # Create an ineligible file in the temporary directory
        txt_path = os.path.join(tmpdir, 'test.txt')
        
        # Create a hidden file in the temporary directory
        hidden_path = os.path.join(tmpdir, '.test-hidden.tif')
        
        # Create a TIF file in a subdirectory
        subdir_path = os.path.join(tmpdir, 'subdir')
        os.mkdir(subdir_path)
        tif_path2 = os.path.join(subdir_path, 'mytest456.tif')
        img2 = Image.new('RGB', (100, 100), color='blue')
        img2.save(tif_path2)

        # Process the directory with a pattern
        process_directory(tmpdir, r'test\d+', ImageSize.ORIGINAL, None)

        # Check that only the TIF files at the root level were processed
        png_path = os.path.join(tmpdir, 'test123.png')
        png_path2 = os.path.join(tmpdir, 'CANON12345-ENHANCED-NR.png')
        subdir_png_path = os.path.join(subdir_path, 'test456.png')
        assert os.path.exists(png_path), "PNG file 1 does not exist"
        assert os.path.exists(png_path2), "PNG file 2 does not exist"
        assert not os.path.exists(hidden_path), "Hidden file was processed"
        assert not os.path.exists(subdir_png_path), "File in subdirectory was processed"

def test_process_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create two TIF files in the temporary directory
        tif_path1 = os.path.join(tmpdir, 'test1.tif')
        img1 = Image.new('RGB', (100, 100), color='red')
        img1.save(tif_path1)

        tif_path2 = os.path.join(tmpdir, 'test2.tif')
        img2 = Image.new('RGB', (100, 100), color='blue')
        img2.save(tif_path2)

        # Process the files
        process_files([tif_path1, tif_path2], None, ImageSize.ORIGINAL, None)

        # Check that the PNG files were created
        png_path1 = os.path.join(tmpdir, 'test1.png')
        png_path2 = os.path.join(tmpdir, 'test2.png')
        assert os.path.exists(png_path1), "PNG file 1 does not exist"
        assert os.path.exists(png_path2), "PNG file 2 does not exist"

def test_process_files_with_pattern():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create two TIF files in the temporary directory
        tif_path1 = os.path.join(tmpdir, 'mytest123.tif')
        img1 = Image.new('RGB', (100, 100), color='red')
        img1.save(tif_path1)

        tif_path2 = os.path.join(tmpdir, 'mytest456.tif')
        img2 = Image.new('RGB', (100, 100), color='blue')
        img2.save(tif_path2)
        
        tif_path3 = os.path.join(tmpdir, 'mytest759-ENHANCED-NR.tif')
        img3 = Image.new('RGB', (100, 100), color='green')
        img3.save(tif_path3)

        # Process the files with a pattern
        process_files([tif_path1, tif_path2, tif_path3], r'test\d+', ImageSize.ORIGINAL, None)

        # Check that the PNG files were created with the correct names
        png_path1 = os.path.join(tmpdir, 'test123.png')
        png_path2 = os.path.join(tmpdir, 'test456.png')
        png_path3 = os.path.join(tmpdir, 'test759.png')
        assert os.path.exists(png_path1), "PNG file 1 does not exist"
        assert os.path.exists(png_path2), "PNG file 2 does not exist"
        assert os.path.exists(png_path3), "PNG file 3 does not exist"

def test_process_files_with_log():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a TIF file in the temporary directory
        tif_path = os.path.join(tmpdir, 'test.tif')
        img = Image.new('RGB', (100, 100), color='red')
        img.save(tif_path)

        # Process the file with logging
        log_path = os.path.join(tmpdir, '.log.txt')
        process_files([tif_path], None, ImageSize.ORIGINAL, log_path)

        # Check that the log file was created
        assert os.path.exists(log_path), "Log file does not exist"
        
def test_process_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a TIF file in the temporary directory
        tif_path = os.path.join(tmpdir, 'test.tif')
        img = Image.new('RGB', (100, 100), color='red')
        img.save(tif_path)

        # Process the file
        process_file(tif_path, 'test', ImageSize.ORIGINAL, None)

        # Check that the PNG file was created
        png_path = os.path.join(tmpdir, 'test.png')
        assert os.path.exists(png_path), "PNG file does not exist"

def test_log_message():
    with tempfile.TemporaryDirectory() as tmpdir:
        # Log a message
        log_path = os.path.join(tmpdir, '.log.txt')
        log_message('Test message', log_path)

        # Check that the log file was created
        assert os.path.exists(log_path), "Log file does not exist"
