#!python3
# -*- coding: utf-8 -*-
# Simple script that open for you a google map with a marker pointing to a place
# where given photo have been taken (if there are coordinates in EXIF of photo)
import exifread
import os


def exif_to_dd(value):
    lat_ref = str(value[0])
    lat = value[1]
    lon_ref = str(value[2])
    lon = value[3]

    def idf_tag_to_coordinate(tag):
        # convert ifdtag from exifread module to decimal degree coordinate
        tag = str(tag).replace('[', '').replace(']', '').split(',')
        tag[2] = int(tag[2].split('/')[0]) / int(tag[2].split('/')[1])
        return int(tag[0]) + int(tag[1])/60 + tag[2]/3600

    # Return positive ir negative longitude/latitude from exifread's ifdtag
    lat = -(idf_tag_to_coordinate(lat)) if lat_ref == 'S' else idf_tag_to_coordinate(lat)
    lon = -(idf_tag_to_coordinate(lon)) if lon_ref == 'E' else idf_tag_to_coordinate(lon)

    print('GPS coordinates in decimal degrees format:')
    print('Latitude: ' + str(lat))
    print('Longitude: ' + str(lon))
    print('Query for Google Maps:')
    print('https://www.google.com/maps/?q={:.5f},{:.5f} '.format(lat, lon))
    return lat, lon


def read_exif(file):
    with open(file, 'rb') as image:
        tags = exifread.process_file(image, details=False)
        if len(tags.keys()) < 1:
            print('The is no EXIF in this file.')
            exit()

        raw_coordinates = [tags['GPS GPSLatitudeRef'],
                           tags['GPS GPSLatitude'],
                           tags['GPS GPSLongitudeRef'],
                           tags['GPS GPSLongitude']]

        exif_to_dd(raw_coordinates)


while True:
    file_path = input('Please type in path to photo: ')
    if os.path.exists(file_path):
        print('Gotcha!')
        read_exif(file_path)
        break
    else:
        print('There is no such file. Try another.')
        continue
