import Common as common
import cv2 as opencv

class TemplateMatching:
        
    template = None    
    
    def __init__(self):         
        # Init windows. One displays the reference, 
        # and the other shows the matching result
        opencv.namedWindow(common.template_preview_window_name, 
                           opencv.WINDOW_AUTOSIZE)
        opencv.namedWindow(common.match_result_window_name, 
                           opencv.WINDOW_AUTOSIZE)

    def set_template(self, current_camera_frame, user_rectangle):
        if(current_camera_frame is not None):
            self.template = current_camera_frame[
                user_rectangle[1]:user_rectangle[3], 
                user_rectangle[0]:user_rectangle[2]]
        
        opencv.imshow(common.template_preview_window_name, 
                        self.template)

    def has_template(self):
        return self.template is not None
    
    def clear_template(self):
        self.template = None       

    def match(self, current_camera_frame):
        if(self.template is not None):
            # Perform template matching
            match_result = opencv.matchTemplate(
                current_camera_frame, self.template, 
                opencv.TM_CCOEFF_NORMED)

            # Display matching result
            opencv.imshow(common.match_result_window_name, match_result)

            return self.draw_tracking_result(match_result, current_camera_frame)
        else:
            return None

    def draw_tracking_result(self, match_result, current_camera_frame):
        # Find min, max and their locations
        (min, max, min_loc, max_loc) = opencv.minMaxLoc(match_result)

        # Get dimensions of the template
        (ref_width, ref_height, ref_channels) = self.template.shape
    
        # Determine new location of the reference rectangle 
        # to indicate object's movement
        top_left_corner = (max_loc[0], max_loc[1])
        bottom_right_corner = (max_loc[0] + ref_height, 
                               max_loc[1] + ref_width)        

        # Adjust color of the rectangle. 
        # The color is green if maximum correlation value is above the threshold
        # Otherwise, the rectangle is red
        corr_threshold = 0.7

        if(max > corr_threshold):
            color = common.green
        else:
            color = common.red
        
        # Draw rectangle
        opencv.rectangle(current_camera_frame, top_left_corner, 
                         bottom_right_corner, color, 
                         common.rectangle_thickness)

        return current_camera_frame

    def release(self):
        self.clear_template()