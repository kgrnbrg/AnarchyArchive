#!/usr/bin/env python
import logging
import random
import urllib
import PIL
import datetime
import tumblr
from bs4 import BeautifulSoup
from argparse import ArgumentParser


# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(name)s [%(levelname)s]: %(message)s')
logger = logging.getLogger("The Art & Science of Whatever::Image Glitch")


class Glitch(object):

    def get_random_start_and_end_points_in_file(self, file_data):
        """ Shortcut method for getting random start and end points in a file """
        start_point = random.randint(2500, len(file_data))
        end_point = start_point + random.randint(0, len(file_data) - start_point)

        return start_point, end_point

    def splice_a_chunk_in_a_file(self, file_data, glitch_num):
        """ Splice a chunk in a file.

        * Picks out a random chunk of the file, duplicates it several times, and then inserts that
        chunk at some other random position in the file.

        """
        start_point, end_point = self.get_random_start_and_end_points_in_file(file_data)
        section = file_data[start_point:end_point]
        repeated = ''

        for i in range(1, glitch_num):
            repeated += section

        new_start_point, new_end_point = self.get_random_start_and_end_points_in_file(file_data)
        file_data = file_data[:new_start_point] + repeated + file_data[new_end_point:]
        return file_data


    def glitch_an_image(self, local_image):
        """ Glitch!

        * Opens the original image file, reads its contents and stores them as 'file_data'
        * Calls 'splice_a_chunk_in_a_file()' method on the data a random number of times between 1 and 5
        * Writes the new glitched image out to a file

        """
        file_handler = open(local_image, 'r')
        file_data = file_handler.read()
        file_handler.close()
        ##YOUR NEW NUMBER##
        search_num = tumblr.top_hit_num
        # divide by 5,000,000 to normalize the range from [0,5000000] to [0,1]
        # multiply by 5 to increase the range from [0,5]

        #glitch_num = (int)(((search_num / float(1000000)) * 5.0)+1)
        glitch_num = 4
        #Image pre-processing via PIL # TODO
        #local_image = self.additional_image_processing(local_image)
        #print local_image
       

        for i in range(1, glitch_num):
            file_data = self.splice_a_chunk_in_a_file(file_data, glitch_num)

        outputfile = self.append_random_number_to_filename(local_image)
        #print outputfile
        file_handler = open(local_image, 'w')
        file_handler.write(file_data)
        file_handler.close

        return local_image

    def append_random_number_to_filename(self, local_img_file):
        """ Prevent overwriting of original file """
        date = datetime.datetime.now()
        date_string = date.strftime("%m-%d-%Y")
        return "%s-glitched.%s" % (local_img_file.split(".")[0], local_img_file.split(".")[1])

    def trigger(self, local_img_file, keyword):
        print local_img_file
        """ Main trigger function """
        # if not local_img_file:
        #     image_url = self.get_flickr_image(keyword)
        #     local_img_file = self.download_an_image(image_url)
        image_glitch_file = self.glitch_an_image(local_img_file)
        return image_glitch_file
        #logger.info("Finished glitching %s" % image_glitch_file)


def main():
    # Handle args
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "-f", "--file",
        dest="local_img_file",
        help="A local file to glitch.",
        metavar="local_file",
    )
    parser.add_argument(
        "-k", "--keyword",
        dest="keyword",
        help="Keyword to use when fetching image via Flickr. Default = 'random'.",
        default="random",
        metavar="keyword",
    )

    args = parser.parse_args()

    # Start the glitch script
    glitch = Glitch()
    glitch.trigger(args.local_img_file, args.keyword)

if __name__ == '__main__':
    main()
