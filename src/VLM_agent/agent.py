from src.VLM_agent.OwlViT_FastSAM_SAM import find_object_central_pixel
from src.mistral_ai.vlm import run_mistral_vlm


def calibrate_points(points):
    """
    TODO:with depth_photo calibrate the pixel point to  world 3d Descartes point.
    """
    return points



def VLM_agent(user_prompt: str, image_path) -> tuple[bool, None | tuple[int, int]]:
    """
    Launch VLM agent to process visual tasks.
    """
    if user_prompt == "user person":
        return True, (0, 0, 0)  # Return a default coordinate point
    elif user_prompt == "home":
        return True, (1, 1, 1)  # Return a default coordinate point
    elif user_prompt == "spoon rest":
        return True, (2, 2, 2)  # Return a default coordinate point

    print("🟢 Starting VLM Agent...")
    if_find , target_label, target_text = run_mistral_vlm(user_prompt, image_path)  # Call VLM model to process visual tasks
    
    if not if_find:
        print("❌ No target found at the moment.")
        return False, None
    
    target_prompt, box_center_point, seg_center_point, bbox, score = find_object_central_pixel(target_label, target_text, image_path, is_sam = True, if_translate = False)  # 调用函数处理图像中的目标检测
    print(f"🔍 Detected target: {target_label}")
    print(f"📍 Target prompt: {target_prompt}")
    print(f"📏 Bounding box: {bbox}")
    print(f"🎯 Box center point: {box_center_point}")
    print(f"🎯 Segmentation center point: {seg_center_point}")
    print(f"📊 Detection score: {score}")

    print("✅ VLM Agent completed.")

    return True, seg_center_point  # Return detected target box and center point coordinates