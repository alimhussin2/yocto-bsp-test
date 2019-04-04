#!/usr/bin/python3

import os
import re
import subprocess

class VideoPlayback():
    def getDriverPlugins(driver):
        if driver == 'msdk' or driver == 'vaapi':
            cmd = 'gst-inspect-1.0 %s' % driver                                                                                                                                          
            with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as p:                                                                               
                return p.communicate()[0].decode()
        else:
            print('Error: %s is not an expected driver' % driver)

    def getFps():
        # TODO: Get FPS of video playback
        pass

    def validateFrame(frame):
        #TODO:  if nth frame is black, then test failed as not image render on screen
        pass

    def runCmd(self, cmd):
        ret = 0
        with subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1024) as p, open('debug_videoplayback.log', 'a+') as f:
            try:
                stdout, stderr = p.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                p.kill()
                stdout, stderr = p.communicate()
                f.write('\ncmd: %s' % cmd)
                f.write(stdout.decode())
                f.close()
                ret = p.returncode
        self.decision(ret, cmd)

    def decision(self, ret, cmd):
        with open('results_videoplayback.log', 'a+') as f:
            if ret == 0:
                status = "FAIL"
                print('Test: %s : %s' % (cmd, status))
                print('Return code: %s' % ret)
            elif ret == -9:
                status = "PASS"
                print('Test: %s : %s' % (cmd, status))
                print('Return code: %s' % ret)
            else:
                status = "FAIL"
                print('Test: %s : %s' % (cmd, status))
                print('Return code: %s' % ret)
            f.write('Test: %s : %s\n' % (cmd, status))
            f.write('Return code : %s\n' % ret)
            f.close()

class FpsH264VideoPlayback(VideoPlayback):                                                                                                                                                                
    def __init__(self, driver):                               
        self.driver = driver                                                                                                                                                                              
                                                                                                                                                                              
    def run(self, videofile):                                                                                                                                                                      
        if self.driver == "vaapi":                                                                                                                                                                 
            cmd = 'gst-launch-1.0 -v filesrc location=%s ! qtdemux ! h264parse ! vaapih264dec ! fpsdisplaysink video-sink="xvimagesink render-rectangle=<0,0,1920,1080>"' % videofile                     
        elif self.driver == "msdk":                           
            cmd = 'LIBVA_DRIVER_NAME=iHD gst-launch-1.0 -v filesrc location=%s ! qtdemux ! h264parse ! msdkh264dec ! fpsdisplaysink video-sink="glimagesink render-rectangle=<0,0,1920,1080>"' % videofile
        self.runCmd(cmd)                                       
                                                                                                                                                                                                   
    def test_H264_1080p60_8bitsVideoPlayback(self, videofile):                                        
        self.run(videofile)                                                                                                                                                                               
                                                        
    def test_H264_1080p60_10bitsVideoPlayback(self, videofile):                                                                                                                                    
        self.run(videofile)                                    
                                                                                                                                                                                                   
    def test_H264_2160p60_10bitsVideoPlayback(self, videofile):                                       
        self.run(videofile) 

class FpsH265VideoPlayback(VideoPlayback):
    def __init__(self, driver):
        self.driver = driver

    def run(self, videofile):
        if self.driver == "vaapi":                                                                                                                                                         
            cmd = 'gst-launch-1.0 -v filesrc location=%s ! qtdemux ! h265parse ! vaapih265dec ! fpsdisplaysink video-sink="xvimagesink render-rectangle=<0,0,1920,1080>"' % videofile
        elif self.driver == "msdk":                                                                                                                                                        
            cmd = 'LIBVA_DRIVER_NAME=iHD gst-launch-1.0 -v filesrc location=%s ! qtdemux ! h265parse ! msdkh265dec ! fpsdisplaysink video-sink="glimagesink render-rectangle=<0,0,1920,1080>"' % videofile
        self.runCmd(cmd)         

    def test_H265_1080p60_8bitsVideoPlayback(self, videofile):
        self.run(videofile)

    def test_H265_1080p60_10bitsVideoPlayback(self, videofile):
        self.run(videofile)

    def test_H265_2160p60_10bitsVideoPlayback(self, videofile):
        self.run(videofile)

class FpsVP8VideoPlayback(VideoPlayback):
    def __init__(self, driver):
        self.driver = driver

    def run(self, videofile):
        if self.driver == "vaapi":
            cmd = 'gst-launch-1.0 -v filesrc location=%s ! matroskademux ! vaapivp8dec ! fpsdisplaysink video-sink="xvimagesink render-rectangle=<0,0,1920,1080>"' % videofile
        elif self.driver == "msdk":
            cmd = 'LIBVA_DRIVER_NAME=iHD gst-launch-1.0 -v filesrc location=%s ! matroskademux ! msdkvp8dec ! fpsdisplaysink video-sink="glimagesink render-rectangle=<0,0,1920,1080>"' % videofile
        self.runCmd(cmd)

    def test_VP8_1080p24_VideoPlayback(self, videofile):
        self.run(videofile)

class FpsVP9VideoPlayback(VideoPlayback):                                                                                                                                                                 
    def __init__(self, driver):                                                                                                                                                                           
        self.driver = driver                                                                                                                                                                              
                                                               
    def run(self, videofile):                                  
        if self.driver == "vaapi":                                                                                                                                                   
            cmd = 'gst-launch-1.0 -v filesrc location=%s ! matroskademux ! vaapivp9dec ! fpsdisplaysink video-sink="xvimagesink render-rectangle=<0,0,1920,1080>"' % videofile
        elif self.driver == "msdk":                                                                                                                                                                       
            cmd = 'LIBVA_DRIVER_NAME=iHD gst-launch-1.0 -v filesrc location=%s ! matroskademux ! msdkvp9dec ! fpsdisplaysink video-sink="glimagesink render-rectangle=<0,0,1920,1080>"' % videofile
        self.runCmd(cmd)                                                                                                                                                                           
                                                                                                                                                                                                   
    def test_VP9_1080p30_VideoPlayback(self, videofile):                                                                                                                                           
        self.run(videofile)

    def test_VP9_2160p30_VideoPlayback(self, videofile):
        self.run(videofile)

def test_decoderDriver(hwAccelerator):
    drivers = VideoPlayback.getDriverPlugins(hwAccelerator)
    print("Testing %s driver" % hwAccelerator)
    h264dec = hwAccelerator + 'h264dec'
    h265dec = hwAccelerator + 'h265dec'
    vp8dec = hwAccelerator + 'vp8dec'
    vp9dec = hwAccelerator + 'vp9dec'
    vp10dec = hwAccelerator + 'vp10dec'

    if re.search(h264dec, drivers) is not None:
        print('%s is supported' % h264dec)
        vh264 = FpsH264VideoPlayback(hwAccelerator)
        vh264.test_H264_1080p60_8bitsVideoPlayback("/run/media/sda1/phoronix-cache/download-cache/sample_video/ToS_1080p_59.94fps_H264_25000kbps_8bits_noHDR_v1511090000.mp4")
        vh264.test_H264_2160p60_10bitsVideoPlayback("/run/media/sda1/phoronix-cache/download-cache/sample_video/ToS_2160p_59.94fps_H264_35000kbps_8bits_noHDR_v1511090000.mp4")
    else:
        print('%s is not supported' % h264)

    if re.search(h265dec, drivers) is not None:
        print('%s is supported' % h265dec)
        vh265 = FpsH265VideoPlayback(hwAccelerator)
        vh265.test_H265_1080p60_8bitsVideoPlayback("/run/media/sda1/phoronix-cache/download-cache/sample_video/ToS_1080p_59.94fps_H265_12000kbps_8bits_noHDR_v1511090000.mp4")
        vh265.test_H265_1080p60_10bitsVideoPlayback("/run/media/sda1/phoronix-cache/download-cache/sample_video/ToS_1080p_59.94fps_H265_12000kbps_10bits_noHDR_v1511090000.mp4")
        vh265.test_H265_2160p60_10bitsVideoPlayback("/run/media/sda1/phoronix-cache/download-cache/sample_video/ToS_2160p_59.94fps_H265_35000kbps_10bits_noHDR_v1511090000.mp4")
    else:                                                                                                                                                                                
        print('%s is not supported' % h265dec)

    if re.search(vp8dec, drivers) is not None:
        print('%s is supported' % vp8dec)
        vp8 = FpsVP8VideoPlayback(hwAccelerator)
        vp8.test_VP8_1080p24_VideoPlayback("/run/media/sda1/phoronix-cache/download-cache/sample_video/ToS_1080p_24fps_VP8.webm")
    else:
        print('%s is not supported' % vp8dec)

    if re.search(vp9dec, drivers) is not None:                                                                                                                                  
        print('%s is supported' % vp9dec)                                                                                                                                               
        vp9 = FpsVP9VideoPlayback(hwAccelerator)                                                                                                                                
        vp9.test_VP9_1080p30_VideoPlayback("/run/media/sda1/phoronix-cache/download-cache/sample_video/ToS_1080p_29.97fps_VP9_8000kbps_8bits_noHDR_v2014.webm")
        vp9.test_VP9_2160p30_VideoPlayback("/run/media/sda1/phoronix-cache/download-cache/sample_video/ToS_2160p_29.97fps_VP9_35000kbps_8bits_noHDR_v2014.webm")
    else:                                                                                                                                                                       
        print('%s not supported' % vp9dec)

if __name__ == "__main__":
    test_decoderDriver('vaapi')
    test_decoderDriver('msdk')

