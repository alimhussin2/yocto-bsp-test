import logging
import subprocess
from shutil import rmtree
from oeqa.runtime.case import OERuntimeTestCase
from oeqa.core.decorator.oeid import OETestID

class AudioTest(OERuntimeTestCase):
    def generate_fingerprint(self, audio_file):
        output = []
        cmd = subprocess.check_output(['/usr/bin/fpcalc', '-raw', audio_file]).decode()
        output = cmd.split('\n')
        #duration = output[0].replace("DURATION=", "")
        fingerprint = output[1].replace("FINGERPRINT=", "").split(',')
        print(fingerprint)
        return fingerprint

    def check_similarity(self, original_audio, recorded_audio):
        fp_original = self.generate_fingerprint(original_audio)
        fp_recorded = self.generate_fingerprint(recorded_audio)

        match = 0
        mismatch = 0
        index = 0
        rate = 0.0
        sample_length = 0
        total_error = 0
        results = []
        ''' 
        get the duration of audio. Only compare with audio which 
        has lower number of sample. for example original_audio has
        10 samples and recorded has 8 samples, then only compare
        first 8 samples.
        '''
        if len(fp_original) < len(fp_recorded):
            sample_length = int(len(fp_original))
            print('use fp_original length = %d' % sample_length)
        else:
            sample_length = int(len(fp_recorded))
            print('use fp_recorded length = %d' % sample_length)

        for index in range(sample_length):
            result = int(fp_recorded[index]) ^ int(fp_original[index])
            '''
            convert result to binary. Calculate total number of 1.
            To get length of binary use len(format(result, '0b'))
            '''
            bin_result = format(result, '0b')
            num_error = 0
            for z in bin_result:
                if z == '1':
                    num_error += 1
            results.append(result)
            if result == 0:
                match += 1
            else:
                mismatch += 1
            # if more than 50% bits corrupt, then consider the whole fingerprint is corrupt by set all bits to 1
            if num_error >= int(0.5 * len(bin_result)):
                print('corrupt fingerprint [%d], bit length = %d, total corrupted bit = %d' % (index, len(bin_result), num_error,))
                # set all bits to 1
                num_error = len(bin_result)
            total_error += num_error
            index += 1
        length_bin_stream = sample_length * len(bin(int(fp_original[0])))
        accuracy = (length_bin_stream - total_error) / length_bin_stream * 100
        print('accurancy')
        print('length_bin_stream = %d' % length_bin_stream)
        print('total_error = %d' % total_error)
        print('accurancy = %.2f%%' % accuracy)
        return accuracy

    @classmethod
    def setUpClass(cls):
        original_audio = 'sample_audio_16bit.wav'
        src = os.path.join(cls.tc.runtime_files_dir, original_audio)
        dest = '/tmp/%s' % original_audio
        cls.tc.target.copyTo(src, dest)

    def test_audio_over_jack(self):
        passing_rate = 80.0
        self.original_audio = 'sample_audio_16bit.wav'
        self.recorded_audio = 'test_loopback_sample_audio_16bit.wav'
        self.path_original_audio = os.path.join(self.tc.runtime_files_dir, self.original_audio)
        self.path_target_recorded_audio = ('/tmp/%s' % self.recorded_audio)
        # check audio device that connected to host machine. In this case, audio device was connected to DUT.
        cmd_device = "arecord -L | grep -i 'digital audio' | awk -F ' ' '{ print tolower($1) }' > /tmp/audio_device"
        self.device = self.tc.target.run(cmd_device)

        cmd = ('arecord -D `cat /tmp/audio_device`:CARD=CODEC,DEV=0 -f S16_LE -d 8 -r 44100 %s | aplay -t wav  /tmp/%s' % (self.path_target_recorded_audio, self.original_audio))

        status, output = self.tc.target.run(cmd)
        msg = ('Unable to record audio. %s' % output)
        self.assertEqual(status, 0, msg=msg)
        
        workdir = self.tc.runtime_files_dir
        self.path_audio = os.path.join(workdir, 'audio')
        if os.path.exists(self.path_audio):
            rmtree(self.path_audio)
        os.makedirs(self.path_audio)

        # copy from DUT:/tmp/test_loopback_*.wav to ../runtime/files/audio/
        self.target.copyFrom(self.path_target_recorded_audio, self.path_audio)

        self.path_host_recorded_audio = os.path.join(self.path_audio, self.recorded_audio)
        # need a fpcalc install on host machine
        result = self.check_similarity(self.path_original_audio, self.path_host_recorded_audio)
        msg = 'Similarity index is %s' % result
        self.assertGreaterEqual(result, passing_rate, msg=msg)

