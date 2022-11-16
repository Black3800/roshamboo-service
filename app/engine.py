import torch
import os
root = os.path.dirname(os.path.abspath(__file__))

# Model
model = torch.hub.load('ultralytics/yolov5', 'custom', os.path.join(root, '../roshamboo-semi-final-model.pt'))


def inference_from_single_image(path):
    results = model(path)
    results = results.pandas().xyxy[0].to_dict(orient="records")
    if len(results) > 0:
        return results[0]['name']
    else:
        return 'none'


def inference_from_batch(image_paths):
    inference = []
    results = model(image_paths)

    # Loop through each image's result
    for r in results.pandas().xyxy:
        r_inference = r.to_dict(orient="records")
        if len(r_inference) > 0:
            inference.append(r_inference[0]['name'])
        else:
            inference.append('none')
    
    # Return the inferences in the original order
    return inference


# print(inference_from_image('sample-img/sc.jpg'))
# print(inference_from_image('sample-img/rock.jpg'))
# print(inference_from_image('sample-img/paper.jpg'))
# print(inference_from_batch(['sample-img/sc.jpg','sample-img/rock.jpg','sample-img/paper.jpg']))