import torch
import os
root = os.path.dirname(os.path.abspath(__file__))

# Model
model = torch.hub.load('ultralytics/yolov5', 'custom', os.path.join(root, '../roshamboo-final-model.pt'))


def inference_from_single_image(path):
    results = model(path)
    results = results.pandas().xyxy[0].to_dict(orient="records")
    if len(results) > 0:
        return { 'class': results[0]['class'], 'confidence': results[0]['confidence'] }
    else:
        return { 'class': -1, 'confidence': -1 }


def inference_from_batch(image_paths):
    inference = []
    results = model(image_paths)

    # Loop through each image's result
    for r in results.pandas().xyxy:
        r_inference = r.to_dict(orient="records")
        if len(r_inference) > 0:
            inference.append({ 'class': r_inference[0]['class'], 'confidence': r_inference[0]['confidence'] })
        else:
            inference.append({ 'class': -1, 'confidence': -1 })
    
    # Return the inferences in the original order
    return inference


# print(inference_from_image('sample-img/sc.jpg'))
# print(inference_from_image('sample-img/rock.jpg'))
# print(inference_from_image('sample-img/paper.jpg'))
# print(inference_from_batch(['sample-img/sc.jpg','sample-img/rock.jpg','sample-img/paper.jpg']))