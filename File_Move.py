#!/usr/bin/env python3
"""
Scan a designated set of directories for KLA maps to move, then transfer them to the
appropriate production maps directories
Log to file and email a list of interested people on error
"""
__author__ = "Manjunatha Rao"
__version__ = "2018-07-06"
#############
# 2018-07-06: update to use utils CK
#############
# v1.0.1 updated log messages

import os
import shutil
from modules import email
from modules.utils import Utils


def log_and_email(error_text: str):

    logger.error(error_text)
    base_email = email.Email(
        subject=email_subject,
        to_list=email_toList,
    )
    base_email.outro(email_outro)
    base_email.intro(error_text)
    base_email.send()


def copy_maps(source_dir, dest_dir, archive_dir):
    if not os.path.isdir(source_dir):
        error_text = "source_dir {} does not exist".format(source_dir)
        log_and_email(error_text)
        raise FileNotFoundError(error_text)
    if not os.path.isdir(dest_dir):
        error_text = 'dest_dir {} does not exist'.format(dest_dir)
        log_and_email(error_text)
        raise FileNotFoundError(error_text)
    logger.debug('Traversing {}'.format(source_dir))
    none_found = True
    root, dirs, files = next(os.walk(source_dir))  # scan only the directory selected. No recursion.
    for file in files:
        none_found = False
        logger.info('Copying {} \n\tfrom {} \n\tto {}'.format(file, source_dir, dest_dir))
        try:
            shutil.copy(
                os.path.join(root, file),
                os.path.join(dest_dir, file),
            )
        except Exception as err:
            error_text = "Error copying {} \n\tfrom {} \n\tto {}\n\t{}".format(file, source_dir, dest_dir, err)
            log_and_email(error_text)
            raise Exception(err)
        logger.info('Moving {} \n\tfrom {} \n\tto {}'.format(file, source_dir, archive_dir))
        # may be a new channel. No reason to fail for that
        if not os.path.exists(archive_dir):
            os.makedirs(archive_dir)
        try:
            shutil.move(
                os.path.join(root, file),
                os.path.join(archive_dir, file),
            )
        except Exception as err:
            error_text = "Error moving {} \n\tfrom {} \n\tto archive directory {}\n\t{}".format(file, source_dir, archive_dir, err)
            log_and_email(error_text)
            raise Exception(err)
    if none_found:
        logger.debug('No files found')


if __name__ == '__main__':
    utils = Utils(__file__)
    logger = utils.init_logger()
    config = utils.load_config()

    email_toList = config['alert_emails']
    email_subject = config['email_subject']
    email_outro = ''

    map_source = config['map_source']
    map_destination = config['map_destination']
    map_archive = config['archive']

    if config['testing']:
        logger.warning("Testing is TRUE")
        map_source = config['map_source_test']
        map_destination = config['map_destination_test']
        map_archive = config['archive_test']
        email_toList = config['alert_emails_test']
        email_outro = "THIS EMAIL WAS SENT AS A RESULT OF A TEST RUN - SAFE TO DISREGARD"

    logger.debug('map_source: {}\n\tmap_destination: {}\n\tmap_archive: {}'.format(map_source, map_destination, map_archive))

    if not os.path.isdir(map_source):
        error_text = 'Designated map_source directory {} does not exist'.format(map_source)
        log_and_email(error_text)
        raise FileNotFoundError(error_text)
    if not os.path.isdir(map_destination):
        error_text = 'Designated map_destination directory {} does not exist'.format(map_destination)
        log_and_email(error_text)
        raise FileNotFoundError(error_text)
    if not os.path.isdir(map_archive):
        error_text = 'Designated map_archive directory {} does not exist'.format(map_archive)
        log_and_email(error_text)
        raise FileNotFoundError(error_text)

    for channel in config['channel_directories']:
        copy_maps(
            os.path.join(map_source, channel),
            os.path.join(map_destination, channel),
            os.path.join(map_archive, channel)
        )