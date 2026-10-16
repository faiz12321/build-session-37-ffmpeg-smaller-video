"""Small temporary-fixture checks; no production footage or device tests."""
import contextlib
import io
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
import check37
import setup37

GEN = ['ffmpeg','-n','-hide_banner','-nostats','-v','error','-f','lavfi','-i',
       'testsrc=duration=3:size=640x360:rate=24','-f','lavfi','-i',
       'sine=frequency=1000:duration=3','-map','0:v:0','-map','1:a:0',
       '-c:v','libx264','-threads','1','-crf','18','-pix_fmt','yuv420p','-c:a','aac','-b:a','64k','-shortest']
SHRINK = ['ffmpeg','-n','-hide_banner','-nostats','-v','error','-i','input.mp4',
          '-map','0:v:0','-map','0:a:0','-c:v','libx264','-threads','1','-crf','28',
          '-pix_fmt','yuv420p','-c:a','aac','-b:a','64k']

class FixtureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        subprocess.run(GEN + ['input.mp4'],cwd=cls.root,capture_output=True,check=True)
        (cls.root/'input.sha256').write_text(check37.digest(cls.root/'input.mp4')+'\n')
        subprocess.run(SHRINK + ['small.mp4'],cwd=cls.root,capture_output=True,check=True)
    @classmethod
    def tearDownClass(cls): cls.temp.cleanup()
    def test_new_setup(self):
        with tempfile.TemporaryDirectory() as d:
            target=Path(d)/'sample';setup37.make(target);self.assertEqual(list(target.iterdir()),[])
    def test_existing_folder_preserves_nested_data(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'sample';(root/'nested').mkdir(parents=True);p=root/'nested'/'keep';p.write_bytes(b'KEEP');before=(p.read_bytes(),p.stat().st_mtime_ns)
            with self.assertRaises(FileExistsError):setup37.make(root)
            self.assertEqual(before,(p.read_bytes(),p.stat().st_mtime_ns))
    def test_existing_file_preserved(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'sample';p.write_bytes(b'KEEP')
            with self.assertRaises(FileExistsError):setup37.make(p)
            self.assertEqual(p.read_bytes(),b'KEEP')
    def test_fixture_checks(self):
        with contextlib.redirect_stdout(io.StringIO()):check37.check(self.root)
    def test_reencode_preserves_input_bytes_and_mtime(self):
        p=self.root/'input.mp4';before=(check37.digest(p),p.stat().st_mtime_ns)
        subprocess.run(SHRINK+['extra.mp4'],cwd=self.root,capture_output=True,check=True)
        self.assertEqual(before,(check37.digest(p),p.stat().st_mtime_ns))
    def test_existing_output_preserved(self):
        p=self.root/'old.mp4';p.write_bytes(b'KEEP');before=(p.read_bytes(),p.stat().st_mtime_ns)
        result=subprocess.run(SHRINK+['old.mp4'],cwd=self.root,capture_output=True)
        self.assertIn(b'already exists', result.stderr);self.assertEqual(before,(p.read_bytes(),p.stat().st_mtime_ns))
    def test_empty_existing_output_preserved(self):
        p=self.root/'empty.mp4';p.touch();before=p.stat().st_mtime_ns
        result=subprocess.run(SHRINK+['empty.mp4'],cwd=self.root,capture_output=True)
        self.assertIn(b'already exists', result.stderr);self.assertEqual(p.read_bytes(),b'');self.assertEqual(before,p.stat().st_mtime_ns)
    def test_audio_extraction_has_no_video(self):
        subprocess.run(['ffmpeg','-n','-v','error','-i','input.mp4','-vn','-c:a','copy','tone.aac'],cwd=self.root,capture_output=True,check=True)
        info=check37.probe(self.root/'tone.aac');self.assertTrue(info['streams']);self.assertTrue(all(x['codec_type']=='audio' for x in info['streams']))
    def test_missing_input_is_failure(self):
        result=subprocess.run(['ffmpeg','-n','-v','error','-i','missing.mp4','absent.mp4'],cwd=self.root,capture_output=True)
        self.assertTrue(result.stderr.strip());self.assertFalse((self.root/'absent.mp4').exists())
    def test_snapshot_refuses_existing_manifest(self):
        import sys
        with tempfile.TemporaryDirectory() as d:
            r=Path(d);shutil.copyfile(Path(check37.__file__),r/'check37.py');(r/'sample').mkdir();(r/'sample'/'input.mp4').write_bytes(b'input');p=r/'sample'/'input.sha256';p.write_bytes(b'KEEP');before=(p.read_bytes(),p.stat().st_mtime_ns)
            result=subprocess.run([sys.executable,str(r/'check37.py'),'snapshot'],capture_output=True)
            self.assertNotEqual(result.returncode,0);self.assertEqual(before,(p.read_bytes(),p.stat().st_mtime_ns))
    def test_audio_extraction_refuses_existing_output(self):
        p=self.root/'old.aac';p.write_bytes(b'KEEP');before=(p.read_bytes(),p.stat().st_mtime_ns)
        result=subprocess.run(['ffmpeg','-n','-v','error','-i','input.mp4','-vn','-c:a','copy','old.aac'],cwd=self.root,capture_output=True)
        self.assertIn(b'already exists', result.stderr);self.assertEqual(before,(p.read_bytes(),p.stat().st_mtime_ns))
    def test_changed_input_digest_is_detected(self):
        with tempfile.TemporaryDirectory() as d:
            r=Path(d)
            for name in ['input.mp4','small.mp4','input.sha256']:shutil.copyfile(self.root/name,r/name)
            with (r/'input.mp4').open('ab') as h:h.write(b'change')
            with self.assertRaisesRegex(AssertionError,'Input changed'):check37.check(r)

if __name__=='__main__':unittest.main()
