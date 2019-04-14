import argparse
import json

from google.cloud import videointelligence


def analyze_labels(path):
    """ Detects labels given a GCS path. """
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.LABEL_DETECTION]
    operation = video_client.annotate_video(path, features=features)
    print('\nProcessing video for label annotations:')

    result = operation.result(timeout=90)
    print('\nFinished processing.')

    list_of_results = [] 

    segment_labels = result.annotation_results[0].shot_label_annotations
    for i, segment_label in enumerate(segment_labels):
        single_result = {}
        single_result['label_category'] = ''
        single_result['label_description'] = segment_label.entity.description
        # print('Video label description: {}'.format(
        #     segment_label.entity.description))
        if segment_label.category_entities:
            for category_entity in segment_label.category_entities:
                
                if (category_entity.description):
                    single_result['label_category'] = category_entity.description
                # print('\tLabel category description: {}'.format(
                #     category_entity.description))

        for i, segment in enumerate(segment_label.segments):
            start_time = (segment.segment.start_time_offset.seconds +
                          segment.segment.start_time_offset.nanos / 1e9)
            end_time = (segment.segment.end_time_offset.seconds +
                        segment.segment.end_time_offset.nanos / 1e9)
            positions = '{}s to {}s'.format(start_time, end_time)
            confidence = segment.confidence
            # print('\tSegment {}: {}'.format(i, positions))
            # print('\tConfidence: {}'.format(confidence))
            
            single_result["start_time"] = start_time
            single_result["stop_time"] = end_time
            single_result["confidence"] = confidence
            if single_result["confidence"] >= 0.5:
                list_of_results.append(single_result)

        # print('\n')
    return (list_of_results)
