import os
from unittest import TestCase

import numpy as np
from OCC.TopoDS import TopoDS_Shape
from OCC.BRepPrimAPI import BRepPrimAPI_MakeBox

import pygem.stephandler as sh


class TestStepHandler(TestCase):
	def test_step_instantiation(self):
		step_handler = sh.StepHandler()

	def test_step_default_extension_member(self):
		step_handler = sh.StepHandler()
		self.assertListEqual(step_handler.EXTENSIONS, ['.step', '.stp'])

	def test_step_parse_failing_filename_type(self):
		step_handler = sh.StepHandler()
		with self.assertRaises(TypeError):
			mesh_points = step_handler.parse(5.2)

	def test_step_parse_failing_check_extension(self):
		step_handler = sh.StepHandler()
		with self.assertRaises(ValueError):
			mesh_points = step_handler.parse(
				'tests/test_datasets/test_pipe.vtk'
			)

	def test_step_parse_infile(self):
		step_handler = sh.StepHandler()
		mesh_points = step_handler.parse('tests/test_datasets/test_pipe.step')
		self.assertEqual(step_handler.infile, 'tests/test_datasets/test_pipe.step')

	def test_step_parse_control_point_position_member(self):
		step_handler = sh.StepHandler()
		mesh_points = step_handler.parse('tests/test_datasets/test_pipe.step')
		self.assertListEqual(
			step_handler._control_point_position,
			[0, 4, 8, 14, 20, 26, 32]
		)

	def test_step_parse_shape(self):
		step_handler = sh.StepHandler()
		mesh_points = step_handler.parse('tests/test_datasets/test_pipe.step')
		self.assertTupleEqual(mesh_points.shape, (32, 3))

	def test_step_parse_shape_stp(self):
		step_handler = sh.StepHandler()
		mesh_points = step_handler.parse('tests/test_datasets/test_pipe.stp')
		self.assertTupleEqual(mesh_points.shape, (32, 3))

	def test_step_parse_coords_1(self):
		step_handler = sh.StepHandler()
		mesh_points = step_handler.parse('tests/test_datasets/test_pipe.step')
		np.testing.assert_almost_equal(mesh_points[6][0], -1000.0)

	def test_step_parse_coords_2(self):
		step_handler = sh.StepHandler()
		mesh_points = step_handler.parse('tests/test_datasets/test_pipe.step')
		np.testing.assert_almost_equal(mesh_points[8][1], 999.99999997448208)

	def test_step_parse_coords_3(self):
		step_handler = sh.StepHandler()
		mesh_points = step_handler.parse('tests/test_datasets/test_pipe.step')
		print np.max(mesh_points[:, 0])
		print np.max(mesh_points[:, 1])
		print np.max(mesh_points[:, 2])
		print np.min(mesh_points[:, 0])
		print np.min(mesh_points[:, 1])
		print np.min(mesh_points[:, 2])
		np.testing.assert_almost_equal(mesh_points[30][2], 10000.0)

	def test_step_parse_coords_4(self):
		step_handler = sh.StepHandler()
		mesh_points = step_handler.parse('tests/test_datasets/test_pipe.step')
		np.testing.assert_almost_equal(mesh_points[0][0], 0.0)

	def test_step_parse_coords_5(self):
		step_handler = sh.StepHandler()
		mesh_points = step_handler.parse('tests/test_datasets/test_pipe.step')
		np.testing.assert_almost_equal(mesh_points[-1][2], 10000.0)

	def test_step_parse_coords_5_stp(self):
		step_handler = sh.StepHandler()
		mesh_points = step_handler.parse('tests/test_datasets/test_pipe.stp')
		np.testing.assert_almost_equal(mesh_points[-1][2], 10000.0)

	def test_step_write_failing_filename_type(self):
		step_handler = sh.StepHandler()
		mesh_points = step_handler.parse('tests/test_datasets/test_pipe.step')
		with self.assertRaises(TypeError):
			step_handler.write(mesh_points, -2)

	def test_step_write_failing_check_extension(self):
		step_handler = sh.StepHandler()
		mesh_points = step_handler.parse('tests/test_datasets/test_pipe.step')
		with self.assertRaises(ValueError):
			step_handler.write(
				mesh_points, 'tests/test_datasets/test_square.stl'
			)

	def test_step_write_failing_infile_instantiation(self):
		step_handler = sh.StepHandler()
		mesh_points = np.zeros((20, 3))
		with self.assertRaises(RuntimeError):
			step_handler.write(
				mesh_points, 'tests/test_datasets/test_pipe_out.step'
			)

	def test_step_write_outfile(self):
		step_handler = sh.StepHandler()
		mesh_points = step_handler.parse('tests/test_datasets/test_pipe.step')
		outfilename = 'tests/test_datasets/test_pipe_out.step'
		step_handler.write(mesh_points, outfilename)
		self.assertEqual(step_handler.outfile, outfilename)
		self.addCleanup(os.remove, outfilename)

	def test_step_write_outfile_tolerance(self):
		step_handler = sh.StepHandler()
		mesh_points = step_handler.parse('tests/test_datasets/test_pipe.step')
		outfilename = 'tests/test_datasets/test_pipe_out.step'
		step_handler.write(mesh_points, outfilename, 1e-3)
		self.assertEqual(step_handler.tolerance, 1e-3)
		self.addCleanup(os.remove, outfilename)

	def test_step_write_modified_tolerance(self):
		step_handler = sh.StepHandler()
		mesh_points = step_handler.parse('tests/test_datasets/test_pipe.step')
		outfilename = 'tests/test_datasets/test_pipe_out.step'
		step_handler.write(mesh_points, outfilename, 1e-3)
		self.assertEqual(step_handler.outfile, outfilename)
		self.addCleanup(os.remove, outfilename)

	def test_step_write_comparison_step(self):
		step_handler = sh.StepHandler()
		mesh_points = step_handler.parse('tests/test_datasets/test_pipe.step')
		mesh_points[0][0] = 2.2
		mesh_points[5][1] = 4.3
		mesh_points[9][2] = 0.5
		mesh_points[12][0] = 7.2
		mesh_points[16][1] = -1.2
		mesh_points[31][2] = -3.6

		outfilename = 'tests/test_datasets/test_pipe_out.step'
		outfilename_expected = 'tests/test_datasets/test_pipe_out_true.step'

		step_handler.write(mesh_points, outfilename)

		mesh_points = step_handler.parse(outfilename)
		mesh_points_expected = step_handler.parse(outfilename_expected)
		np.testing.assert_array_almost_equal(mesh_points, mesh_points_expected)
		self.addCleanup(os.remove, outfilename)

	def test_step_write_comparison_stp(self):
		step_handler = sh.StepHandler()
		mesh_points = step_handler.parse('tests/test_datasets/test_pipe.stp')
		mesh_points[0][0] = 2.2
		mesh_points[5][1] = 4.3
		mesh_points[9][2] = 0.5
		mesh_points[12][0] = 7.2
		mesh_points[16][1] = -1.2
		mesh_points[31][2] = -3.6

		outfilename = 'tests/test_datasets/test_pipe_out.stp'
		outfilename_expected = 'tests/test_datasets/test_pipe_out_true.stp'

		step_handler.write(mesh_points, outfilename)

		mesh_points = step_handler.parse(outfilename)
		mesh_points_expected = step_handler.parse(outfilename_expected)
		np.testing.assert_array_almost_equal(mesh_points, mesh_points_expected)
		self.addCleanup(os.remove, outfilename)

	def test_step_plot_save_fig(self):
		step_handler = sh.StepHandler()
		mesh_points = step_handler.parse('tests/test_datasets/test_pipe.step')
		step_handler.plot(save_fig=True)
		self.assertTrue(os.path.isfile('tests/test_datasets/test_pipe.png'))
		self.addCleanup(os.remove, 'tests/test_datasets/test_pipe.png')

	def test_step_plot_failing_outfile_type(self):
		step_handler = sh.StepHandler()
		with self.assertRaises(TypeError):
			step_handler.plot(plot_file=3)

	def test_step_show_failing_outfile_type(self):
		step_handler = sh.StepHandler()
		with self.assertRaises(TypeError):
			step_handler.show(show_file=1.1)

	def test_step_load_shape_from_file_raises_wrong_type(self):
		with self.assertRaises(TypeError):
			sh.StepHandler.load_shape_from_file(None)

	def test_step_load_shape_from_file_raises_wrong_extension(self):
		with self.assertRaises(ValueError):
			sh.StepHandler.load_shape_from_file('tests/test_datasets/test_pipe.igs')

	def test_step_load_shape_correct_step(self):
		shape = sh.StepHandler.load_shape_from_file(
			'tests/test_datasets/test_pipe.step'
		)
		self.assertEqual(type(shape), TopoDS_Shape)

	def test_step_load_shape_correct_stp(self):
		shape = sh.StepHandler.load_shape_from_file(
			'tests/test_datasets/test_pipe.stp'
		)
		self.assertEqual(type(shape), TopoDS_Shape)

	def test_step_write_shape_to_file_raises_wrong_type(self):
		with self.assertRaises(TypeError):
			sh.StepHandler.write_shape_to_file(None, None)

	def test_step_write_shape_to_file_raises_wrong_extension(self):
		with self.assertRaises(ValueError):
			sh.StepHandler.load_shape_from_file('tests/test_datasets/x.igs')

	def test_step_write_shape_to_file_step(self):
		shp = BRepPrimAPI_MakeBox(1., 1., 1.).Shape()
		path = 'tests/test_datasets/x.step'
		sh.StepHandler.write_shape_to_file(shp, path)
		self.assertTrue(os.path.exists(path))
		self.addCleanup(os.remove, path)

	def test_step_write_shape_to_file_stp(self):
		shp = BRepPrimAPI_MakeBox(1., 1., 1.).Shape()
		path = 'tests/test_datasets/x.stp'
		sh.StepHandler.write_shape_to_file(shp, path)
		self.assertTrue(os.path.exists(path))
		self.addCleanup(os.remove, path)
