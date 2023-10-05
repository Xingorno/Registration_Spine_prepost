from __future__ import print_function
import os
import subprocess
import unittest
import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
from slicer.util import VTKObservationMixin
import logging
import sys
import SimpleITK as sitk


# from PatchDataset3D_v2 import PatchDataset3D
import numpy as np
import SegmentStatistics
import time
import torch
import sysconfig
import shutil


#
# Reg_Spine_prepost
#

class Reg_Spine_prepost(ScriptedLoadableModule):
    """Uses ScriptedLoadableModule base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def __init__(self, parent):
        ScriptedLoadableModule.__init__(self, parent)
        self.parent.title = "Reg_Spine_prepost"  # TODO: make this more human readable by adding spaces
        self.parent.categories = ["Examples"]  # TODO: set categories (folders where the module shows up in the module selector)
        self.parent.dependencies = []  # TODO: add here list of module names that this module requires
        self.parent.contributors = ["Shuwei (Robarts Research Insitute)"]  # TODO: replace with "Firstname Lastname (Organization)"
        # TODO: update with short description of the module and a link to online module documentation
        self.parent.helpText = """
This is an example of scripted loadable module bundled in an extension.
See more information in <a href="https://github.com/organization/projectname#Reg_Spine_prepost">module documentation</a>.
"""
        # TODO: replace with organization, grant and thanks
        self.parent.acknowledgementText = """
This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc., Andras Lasso, PerkLab,
and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
"""




#
# Reg_Spine_prepostWidget
#

class Reg_Spine_prepostWidget(ScriptedLoadableModuleWidget, VTKObservationMixin):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent=None):
    """
    Called when the user opens the module the first time and the widget is initialized.
    """
    ScriptedLoadableModuleWidget.__init__(self, parent)
    VTKObservationMixin.__init__(self)  # needed for parameter node observation
    self._parameterNode = None
    self._updatingGUIFromParameterNode = False

    slicer.mymod = self

  def setEditedNode(self, node, role='', context=''):
    self.setParameterNode(node)
    return node is not None

  def nodeEditable(self, node):
    return 0.7 if node is not None and node.GetAttribute('ModuleName') == self.moduleName else 0.0

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    self.logic = Reg_Spine_prepostLogic()
    self.logic.logCallback = self.addLog
    self.registrationInProgress = False

    # Instantiate and connect widgets ...

    # Load widget from .ui file (created by Qt Designer).
    # Additional widgets can be instantiated manually and added to self.layout.
    uiWidget = slicer.util.loadUI(self.resourcePath('UI/Reg_Spine_prepost.ui'))
    uiWidget.setMRMLScene(slicer.mrmlScene)

    self.layout.addWidget(uiWidget)
    self.ui = slicer.util.childWidgetVariables(uiWidget)

    self.ui.parameterNodeSelector.addAttribute("vtkMRMLScriptedModuleNode", "ModuleName", self.moduleName)
    self.ui.parameterNodeSelector.setNodeTypeLabel("ElastixParameters", "vtkMRMLScriptedModuleNode")

    for preset in self.logic.getRegistrationPresets():
      self.ui.registrationPresetSelector.addItem(
        f"{preset[RegistrationPresets_Modality]} ({preset[RegistrationPresets_Content]})"
      )

    self.ui.customElastixBinDirSelector.settingKey = self.logic.customElastixBinDirSettingsKey
    self.ui.customElastixBinDirSelector.retrieveHistory()
    self.ui.customElastixBinDirSelector.currentPath = 'C:/Slicer 5.4/slicer.org/Extensions-31938/SlicerElastix/lib/Slicer-5.4'

    # These connections ensure that we update parameter node when scene is closed
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.StartCloseEvent, self.onSceneStartClose)
    self.addObserver(slicer.mrmlScene, slicer.mrmlScene.EndCloseEvent, self.onSceneEndClose)

    # connections
    self.ui.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.ui.showTemporaryFilesFolderButton.connect('clicked(bool)', self.onShowTemporaryFilesFolder)
    self.ui.showRegistrationParametersDatabaseFolderButton.connect('clicked(bool)',
                                                                   self.onShowRegistrationParametersDatabaseFolder)
    self.ui.parameterNodeSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.setParameterNode)
    
    # spine data loading nodes for preprocssing
    self.ui.spineCT_prepost_selector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    
    # self.ui.kidneyCT_prepostSeg_selector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    
    self.ui.pushButtonInitialSegSpine.connect('clicked(bool)', self.onInitialSegmentSpine)
    # self.ui.pushButtonSegRightKidney.connect('clicked(bool)', self.onSegmentRightKidney)
    self.ui.pushButtonCropVertebrae.connect('clicked(bool)', self.onCropSpine)
    # self.ui.pushButtonCropRightKidney.connect('clicked(bool)', self.onCropRightKidney)

    self.ui.checkBox_vertebrae_T1.toggled.connect(self.updateParameterNodeFromGUI)
    self.ui.checkBox_vertebrae_T2.toggled.connect(self.updateParameterNodeFromGUI)
    self.ui.checkBox_vertebrae_T3.toggled.connect(self.updateParameterNodeFromGUI)
    self.ui.checkBox_vertebrae_T4.toggled.connect(self.updateParameterNodeFromGUI)
    self.ui.checkBox_vertebrae_T5.toggled.connect(self.updateParameterNodeFromGUI)
    self.ui.checkBox_vertebrae_T6.toggled.connect(self.updateParameterNodeFromGUI)
    self.ui.checkBox_vertebrae_T7.toggled.connect(self.updateParameterNodeFromGUI)
    self.ui.checkBox_vertebrae_T8.toggled.connect(self.updateParameterNodeFromGUI)
    self.ui.checkBox_vertebrae_T9.toggled.connect(self.updateParameterNodeFromGUI)
    self.ui.checkBox_vertebrae_T10.toggled.connect(self.updateParameterNodeFromGUI)
    self.ui.checkBox_vertebrae_T11.toggled.connect(self.updateParameterNodeFromGUI)
    self.ui.checkBox_vertebrae_T12.toggled.connect(self.updateParameterNodeFromGUI)

    self.ui.checkBox_vertebrae_L1.toggled.connect(self.updateParameterNodeFromGUI)
    self.ui.checkBox_vertebrae_L2.toggled.connect(self.updateParameterNodeFromGUI)
    self.ui.checkBox_vertebrae_L3.toggled.connect(self.updateParameterNodeFromGUI)
    self.ui.checkBox_vertebrae_L4.toggled.connect(self.updateParameterNodeFromGUI)
    self.ui.checkBox_vertebrae_L5.toggled.connect(self.updateParameterNodeFromGUI)

    # for cropping the volume
    self.ui.spineCT_pre_selector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.spineCT_post_selector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    # for registration
    self.ui.fixedVolumeSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.movingVolumeSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.fixedVolumeMaskSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.movingVolumeMaskSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.outputVolumeSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.outputTransformSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.initialTransformSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.updateParameterNodeFromGUI)
    self.ui.forceDisplacementFieldOutputCheckbox.toggled.connect(self.updateParameterNodeFromGUI)
    self.ui.registrationPresetSelector.currentIndexChanged.connect(self.updateParameterNodeFromGUI)
    self.ui.customElastixBinDirSelector.currentPathChanged.connect(self.onCustomElastixBinDirChanged)
    # Immediately update deleteTemporaryFiles in the logic to make it possible to decide to
    # keep the temporary file while the registration is running
    self.ui.keepTemporaryFilesCheckBox.connect("toggled(bool)", self.onKeepTemporaryFilesToggled)

    self.initializeParameterNode()

  def cleanup(self):
    self.removeObservers()

  def enter(self):
    self.initializeParameterNode()

  def exit(self):
    self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

  def onSceneStartClose(self, caller, event):
    self.setParameterNode(None)

  def onSceneEndClose(self, caller, event):
    if self.parent.isEntered:
      self.initializeParameterNode()

  def initializeParameterNode(self):
    self.setParameterNode(self.logic.getParameterNode() if not self._parameterNode else self._parameterNode)

  def setParameterNode(self, inputParameterNode):
    if inputParameterNode:
      self.logic.setDefaultParameters(inputParameterNode)

    # Unobserve previously selected parameter node and add an observer to the newly selected.
    # Changes of parameter node are observed so that whenever parameters are changed by a script or any other module
    # those are reflected immediately in the GUI.
    if self._parameterNode is not None and self.hasObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent,
                                                            self.updateGUIFromParameterNode):
      self.removeObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)
    self._parameterNode = inputParameterNode
    if self._parameterNode is not None:
      self.addObserver(self._parameterNode, vtk.vtkCommand.ModifiedEvent, self.updateGUIFromParameterNode)

    wasBlocked = self.ui.parameterNodeSelector.blockSignals(True)
    self.ui.parameterNodeSelector.setCurrentNode(self._parameterNode)
    self.ui.parameterNodeSelector.blockSignals(wasBlocked)

    # Initial GUI update
    self.updateGUIFromParameterNode()

  def updateParameterNodeFromGUI(self, caller=None, event=None):
    """
    This method is called when the user makes any change in the GUI.
    The changes are saved into the parameter node (so that they are restored when the scene is saved and loaded).
    """

    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    wasModified = self._parameterNode.StartModify()  # Modify all properties in a single batch

    # for spine segmentation
    self._parameterNode.SetNodeReferenceID(self.logic.SPINECT_PREPOST, self.ui.spineCT_prepost_selector.currentNodeID)

    self._parameterNode.SetParameter(self.logic.VERTEBRAE_L1, str(self.ui.checkBox_vertebrae_L1.checked))
    self._parameterNode.SetParameter(self.logic.VERTEBRAE_L2, str(self.ui.checkBox_vertebrae_L2.checked))
    self._parameterNode.SetParameter(self.logic.VERTEBRAE_L3, str(self.ui.checkBox_vertebrae_L3.checked))
    self._parameterNode.SetParameter(self.logic.VERTEBRAE_L4, str(self.ui.checkBox_vertebrae_L4.checked))
    self._parameterNode.SetParameter(self.logic.VERTEBRAE_L5, str(self.ui.checkBox_vertebrae_L5.checked))

    self._parameterNode.SetParameter(self.logic.VERTEBRAE_T1, str(self.ui.checkBox_vertebrae_T1.checked))
    self._parameterNode.SetParameter(self.logic.VERTEBRAE_T2, str(self.ui.checkBox_vertebrae_T2.checked))
    self._parameterNode.SetParameter(self.logic.VERTEBRAE_T3, str(self.ui.checkBox_vertebrae_T3.checked))
    self._parameterNode.SetParameter(self.logic.VERTEBRAE_T4, str(self.ui.checkBox_vertebrae_T4.checked))
    self._parameterNode.SetParameter(self.logic.VERTEBRAE_T5, str(self.ui.checkBox_vertebrae_T5.checked))
    self._parameterNode.SetParameter(self.logic.VERTEBRAE_T6, str(self.ui.checkBox_vertebrae_T6.checked))
    self._parameterNode.SetParameter(self.logic.VERTEBRAE_T7, str(self.ui.checkBox_vertebrae_T7.checked))
    self._parameterNode.SetParameter(self.logic.VERTEBRAE_T8, str(self.ui.checkBox_vertebrae_T8.checked))
    self._parameterNode.SetParameter(self.logic.VERTEBRAE_T9, str(self.ui.checkBox_vertebrae_T9.checked))
    self._parameterNode.SetParameter(self.logic.VERTEBRAE_T10, str(self.ui.checkBox_vertebrae_T10.checked))
    self._parameterNode.SetParameter(self.logic.VERTEBRAE_T11, str(self.ui.checkBox_vertebrae_T11.checked))
    self._parameterNode.SetParameter(self.logic.VERTEBRAE_T12, str(self.ui.checkBox_vertebrae_T12.checked))

    # for cropping the vertebrae
    self._parameterNode.SetNodeReferenceID(self.logic.SPINECT_PRE, self.ui.spineCT_pre_selector.currentNodeID)
    self._parameterNode.SetNodeReferenceID(self.logic.SPINECT_POST_ALIGNED, self.ui.spineCT_post_selector.currentNodeID)
    
    # for registration
    self._parameterNode.SetNodeReferenceID(self.logic.FIXED_VOLUME_REF, self.ui.fixedVolumeSelector.currentNodeID)
    self._parameterNode.SetNodeReferenceID(self.logic.MOVING_VOLUME_REF, self.ui.movingVolumeSelector.currentNodeID)
    self._parameterNode.SetNodeReferenceID(self.logic.FIXED_VOLUME_MASK_REF, self.ui.fixedVolumeMaskSelector.currentNodeID)
    self._parameterNode.SetNodeReferenceID(self.logic.MOVING_VOLUME_MASK_REF, self.ui.movingVolumeMaskSelector.currentNodeID)
    self._parameterNode.SetNodeReferenceID(self.logic.OUTPUT_VOLUME_REF, self.ui.outputVolumeSelector.currentNodeID)
    self._parameterNode.SetNodeReferenceID(self.logic.OUTPUT_TRANSFORM_REF, self.ui.outputTransformSelector.currentNodeID)
    self._parameterNode.SetNodeReferenceID(self.logic.INITIAL_TRANSFORM_REF, self.ui.initialTransformSelector.currentNodeID)
    self._parameterNode.SetParameter(self.logic.FORCE_GRID_TRANSFORM_PARAM, str(self.ui.forceDisplacementFieldOutputCheckbox.checked))

    registrationPreset = self.logic.getRegistrationPresets()[self.ui.registrationPresetSelector.currentIndex]
    self._parameterNode.SetParameter(self.logic.REGISTRATION_PRESET_ID_PARAM, registrationPreset[RegistrationPresets_Id])

    self._parameterNode.EndModify(wasModified)

  def updateGUIFromParameterNode(self, caller=None, event=None):
    """
    This method is called whenever parameter node is changed.
    The module GUI is updated to show the current state of the parameter node.
    """
    if self._parameterNode is None or self._updatingGUIFromParameterNode:
      return

    # Make sure GUI changes do not call updateParameterNodeFromGUI (it could cause infinite loop)
    self._updatingGUIFromParameterNode = True
    # for the kidney original data
    self.ui.spineCT_prepost_selector.setCurrentNode(self._parameterNode.GetNodeReference(self.logic.SPINECT_PREPOST))
   
    self.ui.checkBox_vertebrae_L1.checked = slicer.util.toBool(self._parameterNode.GetParameter(self.logic.VERTEBRAE_L1))
    self.ui.checkBox_vertebrae_L2.checked = slicer.util.toBool(self._parameterNode.GetParameter(self.logic.VERTEBRAE_L2))
    self.ui.checkBox_vertebrae_L3.checked = slicer.util.toBool(self._parameterNode.GetParameter(self.logic.VERTEBRAE_L3))
    self.ui.checkBox_vertebrae_L4.checked = slicer.util.toBool(self._parameterNode.GetParameter(self.logic.VERTEBRAE_L4))
    self.ui.checkBox_vertebrae_L5.checked = slicer.util.toBool(self._parameterNode.GetParameter(self.logic.VERTEBRAE_L5))
    
    self.ui.checkBox_vertebrae_T1.checked = slicer.util.toBool(self._parameterNode.GetParameter(self.logic.VERTEBRAE_T1))
    self.ui.checkBox_vertebrae_T2.checked = slicer.util.toBool(self._parameterNode.GetParameter(self.logic.VERTEBRAE_T2))
    self.ui.checkBox_vertebrae_T3.checked = slicer.util.toBool(self._parameterNode.GetParameter(self.logic.VERTEBRAE_T3))
    self.ui.checkBox_vertebrae_T4.checked = slicer.util.toBool(self._parameterNode.GetParameter(self.logic.VERTEBRAE_T4))
    self.ui.checkBox_vertebrae_T5.checked = slicer.util.toBool(self._parameterNode.GetParameter(self.logic.VERTEBRAE_T5))
    self.ui.checkBox_vertebrae_T6.checked = slicer.util.toBool(self._parameterNode.GetParameter(self.logic.VERTEBRAE_T6))
    self.ui.checkBox_vertebrae_T7.checked = slicer.util.toBool(self._parameterNode.GetParameter(self.logic.VERTEBRAE_T7))
    self.ui.checkBox_vertebrae_T8.checked = slicer.util.toBool(self._parameterNode.GetParameter(self.logic.VERTEBRAE_T8))
    self.ui.checkBox_vertebrae_T9.checked = slicer.util.toBool(self._parameterNode.GetParameter(self.logic.VERTEBRAE_T9))
    self.ui.checkBox_vertebrae_T10.checked = slicer.util.toBool(self._parameterNode.GetParameter(self.logic.VERTEBRAE_T10))
    self.ui.checkBox_vertebrae_T11.checked = slicer.util.toBool(self._parameterNode.GetParameter(self.logic.VERTEBRAE_T11))
    self.ui.checkBox_vertebrae_T12.checked = slicer.util.toBool(self._parameterNode.GetParameter(self.logic.VERTEBRAE_T12))

    # for cropping the vertebrae
    self.ui.spineCT_pre_selector.setCurrentNode(self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE))
    self.ui.spineCT_post_selector.setCurrentNode(self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED))
    
    # for registration
    self.ui.fixedVolumeSelector.setCurrentNode(self._parameterNode.GetNodeReference(self.logic.FIXED_VOLUME_REF))
    self.ui.movingVolumeSelector.setCurrentNode(self._parameterNode.GetNodeReference(self.logic.MOVING_VOLUME_REF))
    self.ui.fixedVolumeMaskSelector.setCurrentNode(self._parameterNode.GetNodeReference(self.logic.FIXED_VOLUME_MASK_REF))
    self.ui.movingVolumeMaskSelector.setCurrentNode(self._parameterNode.GetNodeReference(self.logic.MOVING_VOLUME_MASK_REF))
    self.ui.initialTransformSelector.setCurrentNode(self._parameterNode.GetNodeReference(self.logic.INITIAL_TRANSFORM_REF))

    self.ui.outputVolumeSelector.setCurrentNode(self._parameterNode.GetNodeReference(self.logic.OUTPUT_VOLUME_REF))
    self.ui.outputTransformSelector.setCurrentNode(self._parameterNode.GetNodeReference(self.logic.OUTPUT_TRANSFORM_REF))

    self.ui.forceDisplacementFieldOutputCheckbox.checked = \
      slicer.util.toBool(self._parameterNode.GetParameter(self.logic.FORCE_GRID_TRANSFORM_PARAM))

    registrationPresetIndex = \
      self.logic.getRegistrationIndexByPresetId(self._parameterNode.GetParameter(self.logic.REGISTRATION_PRESET_ID_PARAM))
    self.ui.registrationPresetSelector.setCurrentIndex(registrationPresetIndex)

    self.updateApplyButtonState()

    # All the GUI updates are done
    self._updatingGUIFromParameterNode = False

  def onShowTemporaryFilesFolder(self):
    qt.QDesktopServices().openUrl(qt.QUrl("file:///" + self.logic.getTempDirectoryBase(), qt.QUrl.TolerantMode))

  def onShowRegistrationParametersDatabaseFolder(self):
    qt.QDesktopServices().openUrl(qt.QUrl("file:///" + self.logic.registrationParameterFilesDir, qt.QUrl.TolerantMode))

  def onKeepTemporaryFilesToggled(self, toggle):
    self.logic.deleteTemporaryFiles = toggle

  def onApplyButton(self):
    if self.registrationInProgress:
      self.logic.cancelRequested = True
      self.registrationInProgress = False
    else:
      with slicer.util.tryWithErrorDisplay("Failed to compute results.", waitCursor=True):
        self.ui.statusLabel.plainText = ''
        try:
          self.registrationInProgress = True
          self.updateApplyButtonState()

          self.logic.setCustomElastixBinDir(self.ui.customElastixBinDirSelector.currentPath)
          self.logic.deleteTemporaryFiles = not self.ui.keepTemporaryFilesCheckBox.checked
          self.logic.logStandardOutput = self.ui.showDetailedLogDuringExecutionCheckBox.checked
          self.logic.registerVolumesUsingParameterNode(self._parameterNode)

          # Apply computed transform to moving volume if output transform is computed to immediately see registration results
          movingVolumeNode = self.ui.movingVolumeSelector.currentNode()
          if self.ui.outputTransformSelector.currentNode() is not None \
            and movingVolumeNode is not None \
            and self.ui.outputVolumeSelector.currentNode() is None:
            movingVolumeNode.SetAndObserveTransformNodeID(self.ui.outputTransformSelector.currentNode().GetID())
        finally:
          self.registrationInProgress = False
    self.updateApplyButtonState()

  def onInitialSegmentSpine(self):
    
    ##########################################  
    # set up the TotalSegmentator
    ##########################################
    startTime = time.time()
    self.addLog('Initial segmentation processing started')

    # Create new empty folder
    tempFolder = slicer.util.tempDirectory()
    inputFile = tempFolder+"/total-segmentator-input.nii"
    outputSegmentationFolder = tempFolder + "/segmentation"
    
    # check the cuda available 
    if torch.cuda.is_available():
      self.addLog("torch_cuda is available!")

    totalSegmentatorPath = os.path.join(sysconfig.get_path('scripts'), "TotalSegmentator")
    pythonSlicerExecutablePath = shutil.which('PythonSlicer')
    if not pythonSlicerExecutablePath:
        raise RuntimeError("Python was not found")
    totalSegmentatorCommand = [ pythonSlicerExecutablePath, totalSegmentatorPath]

    # Write input volume to file
    # TotalSegmentator requires NIFTI
    self.addLog(f"Writing input file to {inputFile}")
    volumeStorageNode = slicer.mrmlScene.CreateNodeByClass("vtkMRMLVolumeArchetypeStorageNode")
    volumeStorageNode.SetFileName(inputFile)
    volumeStorageNode.UseCompressionOff()
    volumeStorageNode.WriteData(self._parameterNode.GetNodeReference(self.logic.SPINECT_PREPOST))
    volumeStorageNode.UnRegister(None)

    ##########################################  
    # segment all the T- and L- vertebrae
    ########################################## 
    inputVolumeNode = self._parameterNode.GetNodeReference(self.logic.SPINECT_PREPOST)
    options = ["-i", inputFile, "-o", outputSegmentationFolder,"--roi_subset", "vertebrae_L5", "vertebrae_L4", "vertebrae_L3", "vertebrae_L2", "vertebrae_L1", "vertebrae_T12", "vertebrae_T11", "vertebrae_T10", "vertebrae_T9", "vertebrae_T8", "vertebrae_T7", "vertebrae_T6", "vertebrae_T5", "vertebrae_T4", "vertebrae_T3", "vertebrae_T2", "vertebrae_T1"]
    # options = ["-i", inputFile, "-o", outputSegmentationFolder, "--fast","--roi_subset", "vertebrae_T2"]
    # options = ["-i", inputFile, "-o", outputSegmentationFolder, "--roi_subset", "vertebrae_L3", "vertebrae_L2", "vertebrae_L1"]
    self.addLog('Creating segmentations with TotalSegmentator AI...')
    self.addLog(f"Total Segmentator arguments: {options}")
    proc = slicer.util.launchConsoleProcess(totalSegmentatorCommand + options)
    self.logic.logProcessOutput(proc)
    self.addLog('Importing segmentation results...')
    # outputInitialSegmentationNode = slicer.mrmlScene.CreateNodeByClass("vtkMRMLSegmentationNode")
    outputInitialSegmentationNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
    outputInitialSegmentationNode.SetName(self.logic.SPINECT_PRE_SEGMENTATION)
    self.logic.readSegmentationFolder(outputInitialSegmentationNode, outputSegmentationFolder)
    
    # Set source volume - required for DICOM Segmentation export

    outputInitialSegmentationNode.SetNodeReferenceID(outputInitialSegmentationNode.GetReferenceImageGeometryReferenceRole(), inputVolumeNode.GetID())
    outputInitialSegmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(inputVolumeNode)

    # Place segmentation node in the same place as the input volume
    shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)
    inputVolumeShItem = shNode.GetItemByDataNode(inputVolumeNode)
    studyShItem = shNode.GetItemParent(inputVolumeShItem)
    segmentationShItem = shNode.GetItemByDataNode(outputInitialSegmentationNode)
    shNode.SetItemParent(segmentationShItem, studyShItem)

    if self.logic.clearOutputFolder:
        self.addLog("Cleaning up temporary folder...")
        if os.path.isdir(tempFolder):
            shutil.rmtree(tempFolder)
    
    stopTime = time.time()
    self.addLog(f'Processing completed in {stopTime-startTime:.2f} seconds')

  def onSegmentLeftKidney(self):
    
    startTime = time.time()
    self.addLog('Processing started')

    # Create new empty folder
    tempFolder = slicer.util.tempDirectory()

    inputFile = tempFolder+"/total-segmentator-input.nii"
    outputSegmentationFolder = tempFolder + "/segmentation"
    

    # check the cuda available 
    if torch.cuda.is_available():
      self.addLog("torch_cuda is available!")

    totalSegmentatorPath = os.path.join(sysconfig.get_path('scripts'), "TotalSegmentator")
    pythonSlicerExecutablePath = shutil.which('PythonSlicer')
    if not pythonSlicerExecutablePath:
        raise RuntimeError("Python was not found")
    totalSegmentatorCommand = [ pythonSlicerExecutablePath, totalSegmentatorPath]

    # Write input volume to file
    # TotalSegmentator requires NIFTI
    self.addLog(f"Writing input file to {inputFile}")
    volumeStorageNode = slicer.mrmlScene.CreateNodeByClass("vtkMRMLVolumeArchetypeStorageNode")
    volumeStorageNode.SetFileName(inputFile)
    volumeStorageNode.UseCompressionOff()
    volumeStorageNode.WriteData(self._parameterNode.GetNodeReference(self.logic.KIDNEYCT_PREPOST))
    volumeStorageNode.UnRegister(None)

    # Get options
    options = ["-i", inputFile, "-o", outputSegmentationFolder, "--fast", "--roi_subset", "kidney_left"]
    self.addLog('Creating segmentations with TotalSegmentator AI...')
    self.addLog(f"Total Segmentator arguments: {options}")
    proc = slicer.util.launchConsoleProcess(totalSegmentatorCommand + options)
    self.logic.logProcessOutput(proc)
    # load the segmenation node

    self.addLog('Importing segmentation results...')
    outputSegmentationPath = outputSegmentationFolder + "/kidney_left.nii.gz"
    leftKidneySegmentationNode = slicer.util.loadSegmentation(outputSegmentationPath)
    leftKidneySegmentationNode.SetName("kidney_left_Seg")

    # Place segmentation node in the same place as the input volume
    shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)
    inputVolumeShItem = shNode.GetItemByDataNode(self._parameterNode.GetNodeReference(self.logic.KIDNEYCT_PREPOST))
    studyShItem = shNode.GetItemParent(inputVolumeShItem)
    segmentationShItem = shNode.GetItemByDataNode(leftKidneySegmentationNode)
    shNode.SetItemParent(segmentationShItem, studyShItem)
    stopTime = time.time()
    self.addLog(f'Processing completed in {stopTime-startTime:.2f} seconds')
    
  
  def onSegmentRightKidney(self):
    startTime = time.time()
    self.addLog('Processing started (Right kidney)')

    # Create new empty folder
    tempFolder = slicer.util.tempDirectory()

    inputFile = tempFolder+"/total-segmentator-input.nii"
    outputSegmentationFolder = tempFolder + "/segmentation"
    

    # check the cuda available 
    if torch.cuda.is_available():
      self.addLog("torch_cuda is available!")

    totalSegmentatorPath = os.path.join(sysconfig.get_path('scripts'), "TotalSegmentator")
    pythonSlicerExecutablePath = shutil.which('PythonSlicer')
    if not pythonSlicerExecutablePath:
        raise RuntimeError("Python was not found")
    totalSegmentatorCommand = [ pythonSlicerExecutablePath, totalSegmentatorPath]

    # Write input volume to file
    # TotalSegmentator requires NIFTI
    self.addLog(f"Writing input file to {inputFile}")
    volumeStorageNode = slicer.mrmlScene.CreateNodeByClass("vtkMRMLVolumeArchetypeStorageNode")
    volumeStorageNode.SetFileName(inputFile)
    volumeStorageNode.UseCompressionOff()
    volumeStorageNode.WriteData(self._parameterNode.GetNodeReference(self.logic.KIDNEYCT_PREPOST))
    volumeStorageNode.UnRegister(None)

    # Get options
    options = ["-i", inputFile, "-o", outputSegmentationFolder, "--fast", "--roi_subset", "kidney_right"]
    self.addLog('Creating segmentations with TotalSegmentator AI...')
    self.addLog(f"Total Segmentator arguments: {options}")
    proc = slicer.util.launchConsoleProcess(totalSegmentatorCommand + options)
    self.logic.logProcessOutput(proc)
    # load the segmenation node

    self.addLog('Importing segmentation results...')
    outputSegmentationPath = outputSegmentationFolder + "/kidney_right.nii.gz"
    leftKidneySegmentationNode = slicer.util.loadSegmentation(outputSegmentationPath)
    leftKidneySegmentationNode.SetName("kidney_right_Seg")

    # Place segmentation node in the same place as the input volume
    shNode = slicer.vtkMRMLSubjectHierarchyNode.GetSubjectHierarchyNode(slicer.mrmlScene)
    inputVolumeShItem = shNode.GetItemByDataNode(self._parameterNode.GetNodeReference(self.logic.KIDNEYCT_PREPOST))
    studyShItem = shNode.GetItemParent(inputVolumeShItem)
    segmentationShItem = shNode.GetItemByDataNode(leftKidneySegmentationNode)
    shNode.SetItemParent(segmentationShItem, studyShItem)
    stopTime = time.time()
    self.addLog(f'Processing completed in {stopTime-startTime:.2f} seconds')

  def onCropSpine(self):
    
    if self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE) or self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED):
        self.addLog('Cropping VERTEBRAE_L1')
    else:
        raise ValueError('No pre- or post- volume input!!!')
    
    # load pre/post ct volume node
    inputVolumeNode_pre = self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE)
    inputVolumeNode_post_aligned = self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED)

    initialSegmentationNode = slicer.util.getFirstNodeByName(self.logic.SPINECT_PRE_SEGMENTATION)

    # L1
    if self._parameterNode.GetParameter(self.logic.VERTEBRAE_L1) == 'True':
      
      vertebraeRoi = self.logic.segROI(initialSegmentationNode, self.logic.VERTEBRAE_L1)
      vertebraeRoi.SetName("ROI_"+ self.logic.VERTEBRAE_L1)
      if self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE):
        self.logic.CropVertebrae(inputVolumeNode_pre, vertebraeRoi, self.logic.VERTEBRAE_L1)

      if self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED):
        self.logic.CropVertebrae(inputVolumeNode_post_aligned, vertebraeRoi, self.logic.VERTEBRAE_L1)

    # L2
    if self._parameterNode.GetParameter(self.logic.VERTEBRAE_L2) == 'True':
      vertebraeRoi = self.logic.segROI(initialSegmentationNode, self.logic.VERTEBRAE_L2)
      vertebraeRoi.SetName("ROI_"+ self.logic.VERTEBRAE_L2)
      if self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE):
        self.logic.CropVertebrae(inputVolumeNode_pre, vertebraeRoi, self.logic.VERTEBRAE_L2)

      if self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED):
        self.logic.CropVertebrae(inputVolumeNode_post_aligned, vertebraeRoi, self.logic.VERTEBRAE_L2)
    # L3
    if self._parameterNode.GetParameter(self.logic.VERTEBRAE_L3) == 'True':
      vertebraeRoi = self.logic.segROI(initialSegmentationNode, self.logic.VERTEBRAE_L3)
      vertebraeRoi.SetName("ROI_"+ self.logic.VERTEBRAE_L3)
      if self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE):
        self.logic.CropVertebrae(inputVolumeNode_pre, vertebraeRoi, self.logic.VERTEBRAE_L3)

      if self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED):
        self.logic.CropVertebrae(inputVolumeNode_post_aligned, vertebraeRoi, self.logic.VERTEBRAE_L3)
    
    # L4
    if self._parameterNode.GetParameter(self.logic.VERTEBRAE_L4) == 'True':
      vertebraeRoi = self.logic.segROI(initialSegmentationNode, self.logic.VERTEBRAE_L4)
      vertebraeRoi.SetName("ROI_"+ self.logic.VERTEBRAE_L4)
      if self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE):
        self.logic.CropVertebrae(inputVolumeNode_pre, vertebraeRoi, self.logic.VERTEBRAE_L4)

      if self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED):
        self.logic.CropVertebrae(inputVolumeNode_post_aligned, vertebraeRoi, self.logic.VERTEBRAE_L4)

    # L5
    if self._parameterNode.GetParameter(self.logic.VERTEBRAE_L5) == 'True':
      vertebraeRoi = self.logic.segROI(initialSegmentationNode, self.logic.VERTEBRAE_L5)
      vertebraeRoi.SetName("ROI_"+ self.logic.VERTEBRAE_L5)
      if self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE):
        self.logic.CropVertebrae(inputVolumeNode_pre, vertebraeRoi, self.logic.VERTEBRAE_L5)

      if self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED):
        self.logic.CropVertebrae(inputVolumeNode_post_aligned, vertebraeRoi, self.logic.VERTEBRAE_L5)

    # T1
    if self._parameterNode.GetParameter(self.logic.VERTEBRAE_T1) == 'True':
      vertebraeRoi = self.logic.segROI(initialSegmentationNode, self.logic.VERTEBRAE_T1)
      vertebraeRoi.SetName("ROI_"+ self.logic.VERTEBRAE_T1)
      if self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE):
        self.logic.CropVertebrae(inputVolumeNode_pre, vertebraeRoi, self.logic.VERTEBRAE_T1)

      if self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED):
        self.logic.CropVertebrae(inputVolumeNode_post_aligned, vertebraeRoi, self.logic.VERTEBRAE_T1)
    # T2
    if self._parameterNode.GetParameter(self.logic.VERTEBRAE_T2) == 'True':
      vertebraeRoi = self.logic.segROI(initialSegmentationNode, self.logic.VERTEBRAE_T2)
      vertebraeRoi.SetName("ROI_"+ self.logic.VERTEBRAE_T2)
      if self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE):
        self.logic.CropVertebrae(inputVolumeNode_pre, vertebraeRoi, self.logic.VERTEBRAE_T2)

      if self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED):
        self.logic.CropVertebrae(inputVolumeNode_post_aligned, vertebraeRoi, self.logic.VERTEBRAE_T2)
    # T3
    if self._parameterNode.GetParameter(self.logic.VERTEBRAE_T3) == 'True':
      vertebraeRoi = self.logic.segROI(initialSegmentationNode, self.logic.VERTEBRAE_T3)
      vertebraeRoi.SetName("ROI_"+ self.logic.VERTEBRAE_T3)
      if self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE):
        self.logic.CropVertebrae(inputVolumeNode_pre, vertebraeRoi, self.logic.VERTEBRAE_T3)

      if self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED):
        self.logic.CropVertebrae(inputVolumeNode_post_aligned, vertebraeRoi, self.logic.VERTEBRAE_T3)
    # T4
    if self._parameterNode.GetParameter(self.logic.VERTEBRAE_T4) == 'True':
      vertebraeRoi = self.logic.segROI(initialSegmentationNode, self.logic.VERTEBRAE_T4)
      vertebraeRoi.SetName("ROI_"+ self.logic.VERTEBRAE_T4)
      if self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE):
        self.logic.CropVertebrae(inputVolumeNode_pre, vertebraeRoi, self.logic.VERTEBRAE_T4)

      if self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED):
        self.logic.CropVertebrae(inputVolumeNode_post_aligned, vertebraeRoi, self.logic.VERTEBRAE_T4)
    # T5
    if self._parameterNode.GetParameter(self.logic.VERTEBRAE_T5) == 'True':
      vertebraeRoi = self.logic.segROI(initialSegmentationNode, self.logic.VERTEBRAE_T5)
      vertebraeRoi.SetName("ROI_"+ self.logic.VERTEBRAE_T5)
      if self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE):
        self.logic.CropVertebrae(inputVolumeNode_pre, vertebraeRoi, self.logic.VERTEBRAE_T5)

      if self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED):
        self.logic.CropVertebrae(inputVolumeNode_post_aligned, vertebraeRoi, self.logic.VERTEBRAE_T5)
    # T6
    if self._parameterNode.GetParameter(self.logic.VERTEBRAE_T6) == 'True':
      vertebraeRoi = self.logic.segROI(initialSegmentationNode, self.logic.VERTEBRAE_T6)
      vertebraeRoi.SetName("ROI_"+ self.logic.VERTEBRAE_T6)
      if self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE):
        self.logic.CropVertebrae(inputVolumeNode_pre, vertebraeRoi, self.logic.VERTEBRAE_T6)

      if self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED):
        self.logic.CropVertebrae(inputVolumeNode_post_aligned, vertebraeRoi, self.logic.VERTEBRAE_T6)
    # T7
    if self._parameterNode.GetParameter(self.logic.VERTEBRAE_T7) == 'True':
      vertebraeRoi = self.logic.segROI(initialSegmentationNode, self.logic.VERTEBRAE_T7)
      vertebraeRoi.SetName("ROI_"+ self.logic.VERTEBRAE_T7)
      if self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE):
        self.logic.CropVertebrae(inputVolumeNode_pre, vertebraeRoi, self.logic.VERTEBRAE_T7)

      if self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED):
        self.logic.CropVertebrae(inputVolumeNode_post_aligned, vertebraeRoi, self.logic.VERTEBRAE_T7)
    # T8
    if self._parameterNode.GetParameter(self.logic.VERTEBRAE_T8) == 'True':
      vertebraeRoi = self.logic.segROI(initialSegmentationNode, self.logic.VERTEBRAE_T8)
      vertebraeRoi.SetName("ROI_"+ self.logic.VERTEBRAE_T8)
      if self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE):
        self.logic.CropVertebrae(inputVolumeNode_pre, vertebraeRoi, self.logic.VERTEBRAE_T8)

      if self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED):
        self.logic.CropVertebrae(inputVolumeNode_post_aligned, vertebraeRoi, self.logic.VERTEBRAE_T8)
    # T9
    if self._parameterNode.GetParameter(self.logic.VERTEBRAE_T9) == 'True':
      vertebraeRoi = self.logic.segROI(initialSegmentationNode, self.logic.VERTEBRAE_T9)
      vertebraeRoi.SetName("ROI_"+ self.logic.VERTEBRAE_T9)
      if self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE):
        self.logic.CropVertebrae(inputVolumeNode_pre, vertebraeRoi, self.logic.VERTEBRAE_T9)

      if self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED):
        self.logic.CropVertebrae(inputVolumeNode_post_aligned, vertebraeRoi, self.logic.VERTEBRAE_T9)
    # T10
    if self._parameterNode.GetParameter(self.logic.VERTEBRAE_T10) == 'True':
      vertebraeRoi = self.logic.segROI(initialSegmentationNode, self.logic.VERTEBRAE_T10)
      vertebraeRoi.SetName("ROI_"+ self.logic.VERTEBRAE_T10)
      if self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE):
        self.logic.CropVertebrae(inputVolumeNode_pre, vertebraeRoi, self.logic.VERTEBRAE_T10)

      if self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED):
        self.logic.CropVertebrae(inputVolumeNode_post_aligned, vertebraeRoi, self.logic.VERTEBRAE_T10)
    # T11
    if self._parameterNode.GetParameter(self.logic.VERTEBRAE_T11) == 'True':
      vertebraeRoi = self.logic.segROI(initialSegmentationNode, self.logic.VERTEBRAE_T11)
      vertebraeRoi.SetName("ROI_"+ self.logic.VERTEBRAE_T11)
      if self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE):
        self.logic.CropVertebrae(inputVolumeNode_pre, vertebraeRoi, self.logic.VERTEBRAE_T11)

      if self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED):
        self.logic.CropVertebrae(inputVolumeNode_post_aligned, vertebraeRoi, self.logic.VERTEBRAE_T11)
    # T12
    if self._parameterNode.GetParameter(self.logic.VERTEBRAE_T12) == 'True':
      vertebraeRoi = self.logic.segROI(initialSegmentationNode, self.logic.VERTEBRAE_T12)
      vertebraeRoi.SetName("ROI_"+ self.logic.VERTEBRAE_T12)
      if self._parameterNode.GetNodeReference(self.logic.SPINECT_PRE):
        self.logic.CropVertebrae(inputVolumeNode_pre, vertebraeRoi, self.logic.VERTEBRAE_T12)

      if self._parameterNode.GetNodeReference(self.logic.SPINECT_POST_ALIGNED):
        self.logic.CropVertebrae(inputVolumeNode_post_aligned, vertebraeRoi, self.logic.VERTEBRAE_T12)
    
    slicer.app.processEvents() 
    self.addLog('Cropping completed!')



  def onCropLeftKidney(self):

    # load pre/post ct volume node
    PrePostVolumeNode = self._parameterNode.GetNodeReference(self.logic.KIDNEYCT_PREPOST)

    # load left segmentation node, first needs to convert to labelmap node
    leftSegVolumeNode = self._parameterNode.GetNodeReference(self.logic.KIDNEYCTSEG_PREPOST)
    leftLabelmapNode = slicer.mrmlScene.AddNewNodeByClass('vtkMRMLLabelMapVolumeNode')
    volumes_logic = slicer.modules.volumes.logic()
    volumes_logic.CreateLabelVolumeFromVolume(slicer.mrmlScene, leftLabelmapNode, leftSegVolumeNode)

    leftSegNode = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLSegmentationNode")
    slicer.modules.segmentations.logic().ImportLabelmapToSegmentationNode(leftLabelmapNode, leftSegNode)
    leftSegNode.CreateClosedSurfaceRepresentation()
    leftSegNode.SetName("left_segmentation")
    slicer.mrmlScene.RemoveNode(leftLabelmapNode)

    roi = self.logic.segROI(leftSegNode)
    cropVolumeParameters = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLCropVolumeParametersNode")
    cropVolumeParameters.SetInputVolumeNodeID(PrePostVolumeNode.GetID())
    cropVolumeParameters.SetROINodeID(roi.GetID())
    slicer.modules.cropvolume.logic().Apply(cropVolumeParameters)
    croppedCT = cropVolumeParameters.GetOutputVolumeNode()
    leftSegNode.SetReferenceImageGeometryParameterFromVolumeNode(croppedCT)
    segLogic = slicer.modules.segmentations.logic()
    labelmap = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLLabelMapVolumeNode")
    segLogic.ExportAllSegmentsToLabelmapNode(leftSegNode, labelmap, slicer.vtkSegmentation.EXTENT_REFERENCE_GEOMETRY)
    # slicer.util.saveNode(croppedCT, f"E:/PROGRAM/Project_PhD/TumorCoverage_Renal/dataset/clinical_data/Results/KidneySeg/cropped/test.nii.gz")
    slicer.app.processEvents()
    # print("To do list")

  def onCropRightKidney(self):
    # load pre/post ct volume node
    PrePostVolumeNode = self._parameterNode.GetNodeReference(self.logic.KIDNEYCT_PREPOST)

    print("To do list")


  def updateApplyButtonState(self):

    # update the segmentation node state

    if (self._parameterNode.GetParameter(self.logic.VERTEBRAE_T1) == 'True') or (self._parameterNode.GetParameter(self.logic.VERTEBRAE_T1) == 'True') or \
       (self._parameterNode.GetParameter(self.logic.VERTEBRAE_T3) == 'True') or (self._parameterNode.GetParameter(self.logic.VERTEBRAE_T4) == 'True') or \
       (self._parameterNode.GetParameter(self.logic.VERTEBRAE_T5) == 'True') or (self._parameterNode.GetParameter(self.logic.VERTEBRAE_T6) == 'True') or \
       (self._parameterNode.GetParameter(self.logic.VERTEBRAE_T7) == 'True') or (self._parameterNode.GetParameter(self.logic.VERTEBRAE_T8) == 'True') or \
       (self._parameterNode.GetParameter(self.logic.VERTEBRAE_T9) == 'True') or (self._parameterNode.GetParameter(self.logic.VERTEBRAE_T10) == 'True') or \
       (self._parameterNode.GetParameter(self.logic.VERTEBRAE_T11) == 'True') or (self._parameterNode.GetParameter(self.logic.VERTEBRAE_T12) == 'True') or \
       (self._parameterNode.GetParameter(self.logic.VERTEBRAE_L1) == 'True') or (self._parameterNode.GetParameter(self.logic.VERTEBRAE_L2) == 'True') or \
       (self._parameterNode.GetParameter(self.logic.VERTEBRAE_L3) == 'True') or (self._parameterNode.GetParameter(self.logic.VERTEBRAE_L4) == 'True') or \
       (self._parameterNode.GetParameter(self.logic.VERTEBRAE_L5) == 'True'):
       
      self.ui.pushButtonCropVertebrae.enabled = True
    else:
      self.ui.pushButtonCropVertebrae.enabled = False

    if self._parameterNode.GetNodeReference(self.logic.SPINECT_PREPOST):
      self.ui.pushButtonInitialSegSpine.enabled = True
    else:
      self.ui.pushButtonInitialSegSpine.enabled = False

    if self.registrationInProgress or self.logic.isRunning:
      if self.logic.cancelRequested:
        self.ui.applyButton.text = "Cancelling..."
        self.ui.applyButton.enabled = False
      else:
        self.ui.applyButton.text = "Cancel"
        self.ui.applyButton.enabled = True
    else:
      fixedVolumeNode = self._parameterNode.GetNodeReference(self.logic.FIXED_VOLUME_REF)
      movingVolumeNode = self._parameterNode.GetNodeReference(self.logic.MOVING_VOLUME_REF)
      outputVolumeNode = self._parameterNode.GetNodeReference(self.logic.OUTPUT_VOLUME_REF)
      outputTransformNode = self._parameterNode.GetNodeReference(self.logic.OUTPUT_TRANSFORM_REF)
      if not fixedVolumeNode or not movingVolumeNode:
        self.ui.applyButton.text = "Select fixed and moving volumes"
        self.ui.applyButton.enabled = False
      elif fixedVolumeNode == movingVolumeNode:
        self.ui.applyButton.text = "Fixed and moving volume must not be the same"
        self.ui.applyButton.enabled = False
      elif not outputVolumeNode and not outputTransformNode:
        self.ui.applyButton.text = "Select an output volume and/or output transform"
        self.ui.applyButton.enabled = False
      else:
        self.ui.applyButton.text = "Apply"
        self.ui.applyButton.enabled = True

  def addLog(self, text):
    self.ui.statusLabel.appendPlainText(text)
    slicer.app.processEvents()  # force update

  def onCustomElastixBinDirChanged(self, path):
    if os.path.exists(path):
      wasBlocked = self.ui.customElastixBinDirSelector.blockSignals(True)
      self.ui.customElastixBinDirSelector.addCurrentPathToHistory()
      self.ui.customElastixBinDirSelector.blockSignals(wasBlocked)
    self.logic.setCustomElastixBinDir(path)


#
# Reg_Spine_prepostLogic
#


class Reg_Spine_prepostLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """
  SPINECT_PREPOST = "SpineCT_prepost"
  SPINECT_PRE = "SpineCT_pre"
  SPINECT_POST_ALIGNED = "SpineCT_post_aligned"
  # KIDNEYCTSEG_PREPOST = "KidneyCTSeg_prepost"
  SPINECT_PRE_SEGMENTATION = "pre_CT_initial_segmentation"
  
  VERTEBRAE_T1 = "vertebrae_T1"
  VERTEBRAE_T2 = "vertebrae_T2"
  VERTEBRAE_T3 = "vertebrae_T3"
  VERTEBRAE_T4 = "vertebrae_T4"
  VERTEBRAE_T5 = "vertebrae_T5"
  VERTEBRAE_T6 = "vertebrae_T6"
  VERTEBRAE_T7 = "vertebrae_T7"
  VERTEBRAE_T8 = "vertebrae_T8"
  VERTEBRAE_T9 = "vertebrae_T9"
  VERTEBRAE_T10 = "vertebrae_T10"
  VERTEBRAE_T11 = "vertebrae_T11"
  VERTEBRAE_T12 = "vertebrae_T12"
  VERTEBRAE_L1 = "vertebrae_L1"
  VERTEBRAE_L2 = "vertebrae_L2"
  VERTEBRAE_L3 = "vertebrae_L3"
  VERTEBRAE_L4 = "vertebrae_L4"
  VERTEBRAE_L5 = "vertebrae_L5"


  FIXED_VOLUME_REF = "FixedVolume"
  MOVING_VOLUME_REF = "MovingVolume"
  FIXED_VOLUME_MASK_REF = "FixedVolumeMask"
  MOVING_VOLUME_MASK_REF = "MovingVolumeMask"
  OUTPUT_VOLUME_REF = "OutputVolume"
  OUTPUT_TRANSFORM_REF = "OutputTransform"
  FORCE_GRID_TRANSFORM_PARAM = "ForceGridTransform"
  INITIAL_TRANSFORM_REF = "InitialTransform"
  REGISTRATION_PRESET_ID_PARAM = "RegistrationPresetId"

  DEFAULT_PRESET_ID = "default0"

  INPUT_DIR_NAME = "input"
  OUTPUT_RESAMPLE_DIR_NAME = "result-resample"
  OUTPUT_TRANSFORM_DIR_NAME = "result-transform"
  

  
  
  def __init__(self):
    ScriptedLoadableModuleLogic.__init__(self)
    self.clearOutputFolder = True
    self.logCallback = None
    self.isRunning = False
    self.cancelRequested = False
    self.deleteTemporaryFiles = True
    self.logStandardOutput = False
    self.registrationPresets = None
    self.useStandardSegmentNames = True
    self.customElastixBinDirSettingsKey = 'Elastix/CustomElastixPath'
    self.scriptPath = os.path.dirname(os.path.abspath(__file__))
    self.registrationParameterFilesDir = \
      os.path.abspath(os.path.join(self.scriptPath, 'Resources', 'RegistrationParameters'))
    self.elastixBinDir = None # this will be determined dynamically

    import platform
    executableExt = '.exe' if platform.system() == 'Windows' else ''
    self.elastixFilename = 'elastix' + executableExt
    self.transformixFilename = 'transformix' + executableExt
    
    # slicer.mymod = self
    # # ###############################################################################
    # # # temporary testing
    # paths = [(f"E:\\PROGRAM\\Project_PhD\\Registration\\Data\\DISA_data\\{i}.npz", "mov", "fix") for i in range(0, 2)]
    # patchdata = PatchDataset3D(paths, 51, repeats=1)
    # mov = patchdata.__getitem__(0)
    # slicer.util.addVolumeFromArray(np.double(mov))
    # # ###############################################################################

    self.totalSegmentatorLabelTerminology = {
            "spleen": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^78961009^Spleen~^^~Anatomic codes - DICOM master list~^^~^^|",
            "kidney_right": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^64033007^Kidney~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "kidney_left": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^64033007^Kidney~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "gallbladder": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^28231008^Gallbladder~^^~Anatomic codes - DICOM master list~^^~^^|",
            "liver": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^10200004^Liver~^^~Anatomic codes - DICOM master list~^^~^^|",
            "stomach": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^69695003^Stomach~^^~Anatomic codes - DICOM master list~^^~^^|",
            "aorta": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^15825003^Aorta~^^~Anatomic codes - DICOM master list~^^~^^|",
            "inferior_vena_cava": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^64131007^Inferior vena cava~^^~Anatomic codes - DICOM master list~^^~^^|",
            "portal_vein_and_splenic_vein": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^32764006^Portal vein~^^~Anatomic codes - DICOM master list~^^~^^|",
            "pancreas": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^15776009^Pancreas~^^~Anatomic codes - DICOM master list~^^~^^|",
            "adrenal_gland_right": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^23451007^Adrenal gland~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "adrenal_gland_left": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^23451007^Adrenal gland~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "lung_upper_lobe_left": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^45653009^Upper lobe of lung~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "lung_lower_lobe_left": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^90572001^Lower lobe of lung~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "lung_upper_lobe_right": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^45653009^Upper lobe of lung~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "lung_middle_lobe_right": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^72481006^Middle lobe of right lung~^^~Anatomic codes - DICOM master list~^^~^^|",
            "lung_lower_lobe_right": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^90572001^Lower lobe of lung~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_L5": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^49668003^L5 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_L4": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^11994002^L4 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_L3": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^36470004^L3 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_L2": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^14293000^L2 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_L1": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^66794005^L1 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_T12": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^23215003^T12 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_T11": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^12989004^T11 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_T10": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^7610001^T10 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_T9": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^82687006^T9 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_T8": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^11068009^T8 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_T7": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^62487009^T7 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_T6": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^45296009^T6 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_T5": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^56401006^T5 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_T4": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^73071006^T4 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_T3": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^1626008^T3 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_T2": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^53733008^T2 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_T1": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^64864005^T1 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_C7": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^87391001^C7 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_C6": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^36054005^C6 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_C5": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^36978003^C5 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_C4": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^5329002^C4 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_C3": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^113205007^C3 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_C2": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^39976000^C2 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "vertebrae_C1": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^14806007^C1 vertebra~^^~Anatomic codes - DICOM master list~^^~^^|",
            "esophagus": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^32849002^Esophagus~^^~Anatomic codes - DICOM master list~^^~^^|",
            "trachea": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^44567001^Trachea~^^~Anatomic codes - DICOM master list~^^~^^|",
            "heart_myocardium": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^80891009^Heart~^^~Anatomic codes - DICOM master list~^^~^^|",
            "heart_atrium_left": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^82471001^Left atrium~^^~Anatomic codes - DICOM master list~^^~^^|",
            "heart_ventricle_left": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^87878005^Left ventricle~^^~Anatomic codes - DICOM master list~^^~^^|",
            "heart_atrium_right": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^73829009^Right atrium~^^~Anatomic codes - DICOM master list~^^~^^|",
            "heart_ventricle_right": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^53085002^Right ventricle~^^~Anatomic codes - DICOM master list~^^~^^|",
            "pulmonary_artery": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^81040000^Pulmonary artery~^^~Anatomic codes - DICOM master list~^^~^^|",
            "brain": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^12738006^Brain~^^~Anatomic codes - DICOM master list~^^~^^|",
            "iliac_artery_left": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^73634005^Common iliac artery~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "iliac_artery_right": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^73634005^Common iliac artery~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "iliac_vena_left": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^46027005^Common iliac vein~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "iliac_vena_right": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^46027005^Common iliac vein~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "small_bowel": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^30315005^Small Intestine~^^~Anatomic codes - DICOM master list~^^~^^|",
            "duodenum": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^38848004^Duodenum~^^~Anatomic codes - DICOM master list~^^~^^|",
            "colon": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^71854001^Colon~^^~Anatomic codes - DICOM master list~^^~^^|",
            "rib_left_1": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^48535007^First rib~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "rib_left_2": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^78247007^Second rib~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "rib_left_3": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^25888004^Third rib~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "rib_left_4": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^25523003^Fourth rib~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "rib_left_5": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^15339008^Fifth rib~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "rib_left_6": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^59558009^Sixth rib~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "rib_left_7": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^24915002^Seventh rib~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "rib_left_8": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^5953002^Eighth rib~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "rib_left_9": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^22565002^Ninth rib~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "rib_left_10": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^77644006^Tenth rib~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "rib_left_11": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^58830002^Eleventh rib~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "rib_left_12": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^43993008^Twelfth rib~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "rib_right_1": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^48535007^First rib~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "rib_right_2": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^78247007^Second rib~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "rib_right_3": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^25888004^Third rib~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "rib_right_4": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^25523003^Fourth rib~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "rib_right_5": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^15339008^Fifth rib~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "rib_right_6": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^59558009^Sixth rib~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "rib_right_7": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^24915002^Seventh rib~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "rib_right_8": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^5953002^Eighth rib~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "rib_right_9": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^22565002^Ninth rib~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "rib_right_10": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^77644006^Tenth rib~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "rib_right_11": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^58830002^Eleventh rib~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "rib_right_12": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^43993008^Twelfth rib~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "humerus_left": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^85050009^Humerus~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "humerus_right": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^85050009^Humerus~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "scapula_left": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^79601000^Scapula~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "scapula_right": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^79601000^Scapula~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "clavicula_left": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^51299004^Clavicle~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "clavicula_right": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^51299004^Clavicle~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "femur_left": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^71341001^Femur~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "femur_right": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^71341001^Femur~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "hip_left": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^29836001^Hip~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "hip_right": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^29836001^Hip~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "sacrum": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^54735007^Sacrum~^^~Anatomic codes - DICOM master list~^^~^^|",
            "face": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^89545001^Face~^^~Anatomic codes - DICOM master list~^^~^^|",
            "gluteus_maximus_left": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^181674001^Gluteus maximus muscle~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "gluteus_maximus_right": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^181674001^Gluteus maximus muscle~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "gluteus_medius_left": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^78333006^Gluteus medius muscle~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "gluteus_medius_right": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^78333006^Gluteus medius muscle~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "gluteus_minimus_left": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^78333006^Gluteus medius muscle~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "gluteus_minimus_right": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^78333006^Gluteus medius muscle~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "autochthon_left": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^44947003^Erector spinae muscle~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "autochthon_right": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^44947003^Erector spinae muscle~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "iliopsoas_left": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^68455001^Iliopsoas muscle~SCT^7771000^Left~Anatomic codes - DICOM master list~^^~^^|",
            "iliopsoas_right": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^68455001^Iliopsoas muscle~SCT^24028007^Right~Anatomic codes - DICOM master list~^^~^^|",
            "urinary_bladder": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^89837001^Bladder~^^~Anatomic codes - DICOM master list~^^~^^|",

            # SPecification of these codes are still work in progress:
            #"femur": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^71341001^Femur~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"patella": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^64234005^Patella~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"tibia": "",
            #"fibula": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^87342007^Fibula~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"tarsal": "",
            #"metatarsal": "",
            #"phalanges_feet": "",
            #"humerus": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^85050009^Humerus~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"ulna": "",
            #"radius": "",
            #"carpal": "",
            #"metacarpal": "",
            #"phalanges_hand": "",
            #"sternum": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^56873002^Sternum~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"skull": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^89546000^Skull~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"subcutaneous_fat": "",
            #"skeletal_muscle": "",
            #"torso_fat": "",
            #"spinal_cord": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^2748008^Spinal cord~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"lung_covid_infiltrate": "",
            #"intracerebral_hemorrhage": "",
            #"hip_implant": "Segmentation category and type - DICOM master list~SCT^260787004^Physical object~SCT^40388003^Implant~^^~Anatomic codes - DICOM master list~SCT^24136001^Hip joint~SCT^51440002^Right and left|",
            #"coronary_arteries": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^41801008^Coronary artery~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"kidney": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^64033007^Kidney~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"adrenal_gland": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^23451007^Adrenal gland~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"vertebrae_lumbar": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^51282000^Vertebra~^^~Anatomic codes - DICOM master list~SCT^122496007^Lumbar spine~^^|",
            #"vertebrae_thoracic": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^51282000^Vertebra~^^~Anatomic codes - DICOM master list~SCT^122495006^Thoracic spine~^^|",
            #"vertebrae_cervical": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^51282000^Vertebra~^^~Anatomic codes - DICOM master list~SCT^122494005^Cervical spine~^^|",
            #"iliac_artery": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^73634005^Common iliac artery~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"iliac_vena": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^46027005^Common iliac vein~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"ribs": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^113197003^Rib~^^~Anatomic codes - DICOM master list~SCT^39607008^Lung~SCT^24028007^Right|",
            #"scapula": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^79601000^Scapula~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"clavicula": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^51299004^Clavicle~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"hip": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^29836001^Hip~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"gluteus_maximus": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^181674001^Gluteus maximus muscle~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"gluteus_medius": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^78333006^Gluteus medius muscle~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"gluteus_minimus": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^78333006^Gluteus medius muscle~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"autochthon": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^44947003^Erector spinae muscle~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"iliopsoas": "Segmentation category and type - Total Segmentator~SCT^123037004^Anatomical Structure~SCT^68455001^Iliopsoas muscle~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"lung_vessels": "Segmentation category and type - DICOM master list~SCT^85756007^Tissue~SCT^59820001^Blood vessel~^^~Anatomic codes - DICOM master list~SCT^39607008^Lung~SCT^24028007^Right|",
            #"lung_trachea_bronchia": "Segmentation category and type - DICOM master list~SCT^123037004^Anatomical Structure~SCT^110726009^Trachea and bronchus~^^~Anatomic codes - DICOM master list~^^~^^|",
            #"body_trunc": "",
            #"body_extremities": "",
            #"lung_pleural": "",
            #"pleural_effusion": "",
            #"pericardial_effusion": "",
        }
    
  
  def VolumeReslice(self, volume, slicingMatrix, USImg_depth, slabNum = 1, slabMode = 2):
    ### INPUTS
    # volume: vtkImageData, this could be any 3D volume data (CT, MRI or 3D US)
    # slicingTransformation, vtkMatrix4x4
    # USImg_depth: this is specially for calibrated US, the depth info can help us obtain the image size, spacing 
    # slabNum: slabNum = 1 (default), if slabNum > 1; each ouput slice will actually be a composite of N slices
    # slabMode: if slabNum > 1, different slabMode can be chosen (VTK_IMAGE_SLAB_MIN : 0; VTK_IMAGE_SLAB_MAX: 1, VTK_IMAGE_SLAB_MEAN: 2 (default), VTK_IMAGE_SLAB_SUM: 3)

    ### OUTPUTS
    # reslicedImg: vtkImagedata format

    #################################################################################################
    ### Reslicing defination 
    # Reslicing origin: since our 2D US image is spatially tracked, the reslicng origin is determined by the origin of the 2D US image (left-upper corner) + spatially tracked position
    # Reslicing orientation: same as the "slicingTransformation"
    # Resliced image resolution: same as the input 2D US image, which is obtained from "USImg_depth" 
    # Resliced image size: same as the input 2D US image, which is obtained from "USImg_depth"
    # Interpolation mode: "VTK_NEAREST_INTERPOLATION", "VTK_LINEAR_INTERPOLATION", "VTK_CUBIC_INTERPOLATION"
    #################################################################################################

    # Reslicing Origin + orientation
    imageSpacing, mask, imageHeight = self.ReadMetaInfoFromDepthSetting(USImg_depth)
    slicingTransform = vtk.vtkTransform()
    slicingTransform.SetMatrix(slicingMatrix)
    translateXYZ_delta = [(mask[3]-mask[2]+1)*0.5*imageSpacing[0], 0, 0]
    slicingTransform.Translate(translateXYZ_delta)

    # Reslcied image resolution + size
    reslicedResolution = [imageSpacing[0], imageSpacing[1], imageSpacing[1]]
    reslicedSize = [mask(3)-mask(2) + 1, mask(1) - mask(0) + 1] # weight * height

    reslicer = vtk.vtkImageReslice()
    reslicer.SetInputData(volume)
    reslicer.SetResliceTransfrom(slicingTransform)
    reslicer.SetInterpolationModeToCubic()

    reslicer.SetOutputSpacing(reslicedResolution)
    reslicer.SetOutputOrigin(slicingMatrix.GetElement(0, 3) + translateXYZ_delta[0], slicingMatrix.GetElement(1, 3) + translateXYZ_delta[1], slicingMatrix.GetElement(2, 3) + translateXYZ_delta[2])
    reslicer.SetOutputExtent(0, reslicedSize[0], 0, reslicedSize[1], 0, 1)
    reslicer.SetOutputScalarType(-1) # same as the input
    reslicer.Update()
    reslicedImg = reslicer.GetOutput()

    # # initialize the pixels here
    # reslicedImg.AllocateScalars(vtk.VTK_UNSIGNED_CHAR, 1) # image type and number of components
    # volumeNode = slicer.vtkMRMLScalarVolumeNode()
    # volumeNode.SetAndObserveImageData(reslicedImg)
    # volumeNode = slicer.mrmlScene.AddNode(volumeNode)
    # volumeNode.CreateDefaultDisplayNodes()

    return reslicedImg

  def Slice2VolumeRegistration(self):
    # This function is to achieve the registration of 2D US slice with the 3D volume data (3D US, CT or MRI)
    
    # load the inputs (2D US slice, 3D volume, initial transformation)
    fixed = sitk.ReadImage("E:\\PROGRAM\\Project_PhD\\Registration\\Results\\3_slice2volumeRegistration\\LHV\\LHV-06\\test\\USSlice\\Image_0034.mha", sitk.sitkFloat32)
    moving = sitk.ReadImage("E:\\PROGRAM\\Project_PhD\\Registration\\Results\\3_slice2volumeRegistration\\LHV\\LHV-06\\test\\USVolume\\Pre-Ablation_06_0000.mha", sitk.sitkFloat32)

    # Define initial transform
    # initial transformation: from 3DUS-CT/MRI registration
    # center of rotation: defined as the center of fixed image, and the orientation used the LPS(RAS) convention
    fixedOrigin = fixed.GetOrigin()
    fixedSize = fixed.GetSize()
    fixedSpacing = fixed.GetSpacing()
    fixedIJK2LPS_rowMajor = fixed.GetDirection()
    fixedIJK2LPS = np.array([[fixedIJK2LPS_rowMajor[0], fixedIJK2LPS_rowMajor[1], fixedIJK2LPS_rowMajor[2]], [fixedIJK2LPS_rowMajor[3], fixedIJK2LPS_rowMajor[4], fixedIJK2LPS_rowMajor[5]], [fixedIJK2LPS_rowMajor[6], fixedIJK2LPS_rowMajor[7], fixedIJK2LPS_rowMajor[8]]])
    fixedCenter_withoutOrientation = [fixedSize[0]*0.5, fixedSize[1]*0.5, 0] # note that the third dimensionality
    fixedCenter_shift = np.matmul(fixedIJK2LPS, np.array(fixedCenter_withoutOrientation)*np.array(fixedSpacing))
    fixedCenter = fixedOrigin + fixedCenter_shift # in LPS space which considered the orientation of the volume data

    initial_transform = sitk.Euler3DTransform()
    initial_transform.SetCenter(fixedCenter[0], fixedCenter[1], fixedCenter[2])


    # Design the registration method
    registration_method = sitk.ImageRegistrationMethod()
    
    ## set the similarity metric
    registration_method.SetMetricAsMeanSquares()
    
    ## set the optimizer
    registration_method.SetOptimizerAsPowell()

    ## Set the interpolator
    registration_method.SetInterpolator(sitk.sitkNearestNeighbor)

    ## Set the initial transform
    registration_method.SetInitialTransform(initial_transform)

    registration_method.AddCommand(sitk.sitkIterationEvent, lambda: self.command_iteration(registration_method))

    outTx = registration_method.Execute(fixed, moving)

    print("-------")
    print(outTx)
    print(f"Optimizer stop condition: {registration_method.GetOptimizerStopConditionDescription()}")
    print(f" Iteration: {registration_method.GetOptimizerIteration()}")
    print(f" Metric value: {registration_method.GetMetricValue()}")
    
    # print("To do list")

  def command_iteration(self, method):
    print(
      f"{method.GetOptimizerIteration():3} "
        + f"= {method.GetMetricValue():10.5f} "
        + f": {method.GetOptimizerPosition()}"
    )
  def ReadMetaInfoFromDepthSetting(self, depth):
    ## This setting parameters are specially for our US device (Philips iU22) + US probe (C5-1)

    ROILeft = 0
    ROITop = 0
    ROIWidth = 0
    ROIHeight = 0
    self.imageSpacing = np.array([0, 0, 0], dtype='f')
    if depth == 18:
        self.imageSpacing[0:3] = [0.319, 0.319, 1]
        ROILeft = 80
        ROITop = 120
        ROIWidth = 752
        ROIHeight = 564
    elif depth == 16:
        self.imageSpacing[0:3] = [0.286, 0.286, 1]
        ROILeft = 80
        ROITop = 123
        ROIWidth = 752
        ROIHeight = 560
    elif depth == 14:
        self.imageSpacing[0:3] = [0.251, 0.251, 1]
        ROILeft = 79
        ROITop = 127
        ROIWidth = 752
        ROIHeight = 558
    elif depth == 12:
        self.imageSpacing[0:3] = [0.218, 0.218, 1]
        ROILeft = 74
        ROITop = 132
        ROIWidth = 752
        ROIHeight = 550
    elif depth == 11:
        self.imageSpacing[0:3] = [0.200, 0.200, 1]
        ROILeft = 71
        ROITop = 135
        ROIWidth = 752
        ROIHeight = 550
    elif depth == 10:
        self.imageSpacing[0:3] = [0.185, 0.185, 1]
        ROILeft = 71
        ROITop = 140
        ROIWidth = 752
        ROIHeight = 542
    elif depth == 9:
        self.imageSpacing[0:3] = [0.171, 0.171, 1]
        ROILeft = 68
        ROITop = 153
        ROIWidth = 752
        ROIHeight = 526
    elif depth == 8.1:
        self.imageSpacing[0:3] = [0.160, 0.160, 1]
        ROILeft = 71
        ROITop = 162
        ROIWidth = 752
        ROIHeight = 506
    else:
        print("checking the depth of US image!")
    
    self.imageHeight = ROIHeight
    self.mask = np.array([ROITop, ROITop + ROIHeight, ROILeft, ROILeft + ROIWidth])
    return self.imageSpacing, self.mask, self.imageHeight
  
  def CropVertebrae(self, inputVolumeNode, vertebraeROI, vertebraeName):
    cropVolumeParameters = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLCropVolumeParametersNode")
    cropVolumeParameters.SetInputVolumeNodeID(inputVolumeNode.GetID())
    cropVolumeParameters.SetROINodeID(vertebraeROI.GetID())
    slicer.modules.cropvolume.logic().Apply(cropVolumeParameters)
    croppedCT = cropVolumeParameters.GetOutputVolumeNode()
#   initialSegmentationNode.SetReferenceImageGeometryParameterFromVolumeNode(croppedCT)
    croppedCT.SetName(vertebraeName + "_" +inputVolumeNode.GetName())
  
  def segROI(self, segmentationNode, segmentId):
    # Compute bounding boxes
    segStatLogic = SegmentStatistics.SegmentStatisticsLogic()
    segStatLogic.getParameterNode().SetParameter("Segmentation", segmentationNode.GetID())
    segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_origin_ras.enabled",str(True))
    segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_diameter_mm.enabled",str(True))
    segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_direction_ras_x.enabled",str(True))
    segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_direction_ras_y.enabled",str(True))
    segStatLogic.getParameterNode().SetParameter("LabelmapSegmentStatisticsPlugin.obb_direction_ras_z.enabled",str(True))
    segStatLogic.computeStatistics()
    stats = segStatLogic.getStatistics()

    # Draw ROI for each oriented bounding box
    
    # for segmentId in stats["SegmentIDs"]:

    # Get bounding box
    obb_origin_ras = np.array(stats[segmentId,"LabelmapSegmentStatisticsPlugin.obb_origin_ras"])
    obb_diameter_mm = np.array(stats[segmentId,"LabelmapSegmentStatisticsPlugin.obb_diameter_mm"])
    obb_direction_ras_x = np.array(stats[segmentId,"LabelmapSegmentStatisticsPlugin.obb_direction_ras_x"])
    obb_direction_ras_y = np.array(stats[segmentId,"LabelmapSegmentStatisticsPlugin.obb_direction_ras_y"])
    obb_direction_ras_z = np.array(stats[segmentId,"LabelmapSegmentStatisticsPlugin.obb_direction_ras_z"])
    # Create ROI
    segment = segmentationNode.GetSegmentation().GetSegment(segmentId)
    roi=slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsROINode")
    roi.SetName(segment.GetName() + " OBB")
    roi.GetDisplayNode().SetHandlesInteractive(False)  # do not let the user resize the box
    roi.SetSize(obb_diameter_mm * [2, 1.5, 0.8]) # make the ROI twice the size of the segmentation
    # Position and orient ROI using a transform
    obb_center_ras = obb_origin_ras+0.5*(obb_diameter_mm[0] * obb_direction_ras_x + obb_diameter_mm[1] * obb_direction_ras_y + obb_diameter_mm[2] * obb_direction_ras_z)
    boundingBoxToRasTransform = np.row_stack((np.column_stack(((1,0,0), (0,1,0), (0,0,1), obb_center_ras)), (0, 0, 0, 1)))
    boundingBoxToRasTransformMatrix = slicer.util.vtkMatrixFromArray(boundingBoxToRasTransform)
    roi.SetAndObserveObjectToNodeMatrix(boundingBoxToRasTransformMatrix)
    return roi
  
  def readSegmentationFolder(self, outputSegmentation, output_segmentation_dir):
        """
        The method is very slow, but this is the only option for some specialized tasks.
        """

        outputSegmentation.GetSegmentation().RemoveAllSegments()

        # Get color node with random colors
        randomColorsNode = slicer.mrmlScene.GetNodeByID('vtkMRMLColorTableNodeRandom')
        rgba = [0, 0, 0, 0]

        # Get label descriptions if task is provided
        labelValueToSegmentName = {
        1: "vertebrae_L5",
        2: "vertebrae_L4",
        3: "vertebrae_L3",
        4: "vertebrae_L2",
        5: "vertebrae_L1",
        6: "vertebrae_T12",
        7: "vertebrae_T11",
        8: "vertebrae_T10",
        9: "vertebrae_T9",
        10: "vertebrae_T8",
        11: "vertebrae_T7",
        12: "vertebrae_T6",
        13: "vertebrae_T5",
        14: "vertebrae_T4",
        15: "vertebrae_T3",
        16: "vertebrae_T2",
        17: "vertebrae_T1"
        }

        def import_labelmap_to_segmentation(labelmapVolumeNode, segmentName, segmentId):
            updatedSegmentIds = vtk.vtkStringArray()
            updatedSegmentIds.InsertNextValue(segmentId)
            slicer.modules.segmentations.logic().ImportLabelmapToSegmentationNode(labelmapVolumeNode, outputSegmentation, updatedSegmentIds)
            self.setTerminology(outputSegmentation, segmentName, segmentId)
            slicer.mrmlScene.RemoveNode(labelmapVolumeNode)

        # Read each candidate file
        for labelValue, segmentName in labelValueToSegmentName.items():
            self.addLog(f"Importing {segmentName}")
            labelVolumePath = os.path.join(output_segmentation_dir, f"{segmentName}.nii.gz")
            if not os.path.exists(labelVolumePath):
                continue
            labelmapVolumeNode = slicer.util.loadLabelVolume(labelVolumePath, {"name": segmentName})
            randomColorsNode.GetColor(labelValue, rgba)
            segmentId = outputSegmentation.GetSegmentation().AddEmptySegment(segmentName, segmentName, rgba[0:3])
            import_labelmap_to_segmentation(labelmapVolumeNode, segmentName, segmentId)

  def setTerminology(self, segmentation, segmentName, segmentId):
        segment = segmentation.GetSegmentation().GetSegment(segmentId)
        if not segment:
            # Segment is not present in this segmentation
            return
        if segmentName in self.totalSegmentatorLabelTerminology:
            terminologyEntryStr = self.totalSegmentatorLabelTerminology[segmentName]
            segment.SetTag(segment.GetTerminologyEntryTagName(), terminologyEntryStr)
            try:
                label, color = self.getSegmentLabelColor(terminologyEntryStr)
                if self.useStandardSegmentNames:
                    segment.SetName(label)
                # segment.SetColor(color) # change this color 
            except RuntimeError as e:
                self.log(str(e))
  
  def getSegmentLabelColor(self, terminologyEntryStr):
        """Get segment label and color from terminology"""

        def labelColorFromTypeObject(typeObject):
            """typeObject is a terminology type or type modifier"""
            label = typeObject.GetSlicerLabel() if typeObject.GetSlicerLabel() else typeObject.GetCodeMeaning()
            rgb = typeObject.GetRecommendedDisplayRGBValue()
            return label, (rgb[0]/255.0, rgb[1]/255.0, rgb[2]/255.0)

        tlogic = slicer.modules.terminologies.logic()

        terminologyEntry = slicer.vtkSlicerTerminologyEntry()
        tlogic.DeserializeTerminologyEntry(terminologyEntryStr, terminologyEntry)

        numberOfTypes = tlogic.GetNumberOfTypesInTerminologyCategory(terminologyEntry.GetTerminologyContextName(), terminologyEntry.GetCategoryObject())
        foundTerminologyEntry = slicer.vtkSlicerTerminologyEntry()
        for typeIndex in range(numberOfTypes):
            tlogic.GetNthTypeInTerminologyCategory(terminologyEntry.GetTerminologyContextName(), terminologyEntry.GetCategoryObject(), typeIndex, foundTerminologyEntry.GetTypeObject())
            if terminologyEntry.GetTypeObject().GetCodingSchemeDesignator() != foundTerminologyEntry.GetTypeObject().GetCodingSchemeDesignator():
                continue
            if terminologyEntry.GetTypeObject().GetCodeValue() != foundTerminologyEntry.GetTypeObject().GetCodeValue():
                continue
            if terminologyEntry.GetTypeModifierObject() and terminologyEntry.GetTypeModifierObject().GetCodeValue():
                # Type has a modifier, get the color from there
                numberOfModifiers = tlogic.GetNumberOfTypeModifiersInTerminologyType(terminologyEntry.GetTerminologyContextName(), terminologyEntry.GetCategoryObject(), terminologyEntry.GetTypeObject())
                foundMatchingModifier = False
                for modifierIndex in range(numberOfModifiers):
                    tlogic.GetNthTypeModifierInTerminologyType(terminologyEntry.GetTerminologyContextName(), terminologyEntry.GetCategoryObject(), terminologyEntry.GetTypeObject(),
                        modifierIndex, foundTerminologyEntry.GetTypeModifierObject())
                    if terminologyEntry.GetTypeModifierObject().GetCodingSchemeDesignator() != foundTerminologyEntry.GetTypeModifierObject().GetCodingSchemeDesignator():
                        continue
                    if terminologyEntry.GetTypeModifierObject().GetCodeValue() != foundTerminologyEntry.GetTypeModifierObject().GetCodeValue():
                        continue
                    return labelColorFromTypeObject(foundTerminologyEntry.GetTypeModifierObject())
                continue
            return labelColorFromTypeObject(foundTerminologyEntry.GetTypeObject())

        raise RuntimeError(f"Color was not found for terminology {terminologyEntryStr}")
  
  def setDefaultParameters(self, parameterNode):
    """
    Initialize parameter node with default settings.
    """
    if not parameterNode.GetParameter(self.FORCE_GRID_TRANSFORM_PARAM):
      parameterNode.SetParameter(self.FORCE_GRID_TRANSFORM_PARAM, "False")
    if not parameterNode.GetParameter(self.REGISTRATION_PRESET_ID_PARAM):
      parameterNode.SetParameter(self.REGISTRATION_PRESET_ID_PARAM, self.DEFAULT_PRESET_ID)
    
    # initialize the left or right check box
    parameterNode.SetParameter(self.VERTEBRAE_L1, "False")
    parameterNode.SetParameter(self.VERTEBRAE_L2, "False")
    parameterNode.SetParameter(self.VERTEBRAE_L3, "False")
    parameterNode.SetParameter(self.VERTEBRAE_L4, "False")
    parameterNode.SetParameter(self.VERTEBRAE_L5, "False")
    parameterNode.SetParameter(self.VERTEBRAE_T1, "False")
    parameterNode.SetParameter(self.VERTEBRAE_T2, "False")
    parameterNode.SetParameter(self.VERTEBRAE_T3, "False")
    parameterNode.SetParameter(self.VERTEBRAE_T4, "False")
    parameterNode.SetParameter(self.VERTEBRAE_T5, "False")
    parameterNode.SetParameter(self.VERTEBRAE_T6, "False")
    parameterNode.SetParameter(self.VERTEBRAE_T7, "False")
    parameterNode.SetParameter(self.VERTEBRAE_T8, "False")
    parameterNode.SetParameter(self.VERTEBRAE_T9, "False")
    parameterNode.SetParameter(self.VERTEBRAE_T10, "False")
    parameterNode.SetParameter(self.VERTEBRAE_T11, "False")
    parameterNode.SetParameter(self.VERTEBRAE_T12, "False")

  def addLog(self, text):
    logging.info(text)
    if self.logCallback:
      self.logCallback(text)

  def getElastixBinDir(self):
    if self.elastixBinDir:
      return self.elastixBinDir

    self.elastixBinDir = self.getCustomElastixBinDir()
    if self.elastixBinDir:
      return self.elastixBinDir

    elastixBinDirCandidates = [
      # install tree
      os.path.join(self.scriptPath, '..'),
      os.path.join(self.scriptPath, '../../../bin'),
      # build tree
      os.path.join(self.scriptPath, '../../../../bin'),
      os.path.join(self.scriptPath, '../../../../bin/Release'),
      os.path.join(self.scriptPath, '../../../../bin/Debug'),
      os.path.join(self.scriptPath, '../../../../bin/RelWithDebInfo'),
      os.path.join(self.scriptPath, '../../../../bin/MinSizeRel') ]

    for elastixBinDirCandidate in elastixBinDirCandidates:
      if os.path.isfile(os.path.join(elastixBinDirCandidate, self.elastixFilename)):
        # elastix found
        self.elastixBinDir = os.path.abspath(elastixBinDirCandidate)
        return self.elastixBinDir

    raise ValueError('Elastix not found')

  def getCustomElastixBinDir(self):
    return slicer.util.settingsValue(self.customElastixBinDirSettingsKey, '')

  def setCustomElastixBinDir(self, customPath):
    # don't save it if already saved
    settings = qt.QSettings()
    if settings.contains(self.customElastixBinDirSettingsKey):
      if customPath == settings.value(self.customElastixBinDirSettingsKey):
        return
    settings.setValue(self.customElastixBinDirSettingsKey, customPath)
    # Update elastix bin dir
    self.elastixBinDir = None
    self.getElastixBinDir()

  def getElastixEnv(self):
    """Create an environment for elastix where executables are added to the path"""
    elastixBinDir = self.getElastixBinDir()
    elastixEnv = os.environ.copy()
    elastixEnv["PATH"] = os.path.join(elastixBinDir, elastixEnv["PATH"]) if elastixEnv.get("PATH") else elastixBinDir

    import platform
    if platform.system() != 'Windows':
      elastixLibDir = os.path.abspath(os.path.join(elastixBinDir, '../lib'))
      elastixEnv["LD_LIBRARY_PATH"] = os.path.join(elastixLibDir, elastixEnv["LD_LIBRARY_PATH"]) if elastixEnv.get("LD_LIBRARY_PATH") else elastixLibDir

    return elastixEnv

  def getRegistrationPresets(self):
    if self.registrationPresets:
      return self.registrationPresets

    # Read database from XML file
    elastixParameterSetDatabasePath = os.path.join(self.scriptPath, 'Resources', 'RegistrationParameters', 'ElastixParameterSetDatabase.xml')
    if not os.path.isfile(elastixParameterSetDatabasePath):
      raise ValueError("Failed to open parameter set database: "+elastixParameterSetDatabasePath)
    elastixParameterSetDatabaseXml = vtk.vtkXMLUtilities.ReadElementFromFile(elastixParameterSetDatabasePath)

    # Create python list from XML for convenience
    self.registrationPresets = []
    for parameterSetIndex in range(elastixParameterSetDatabaseXml.GetNumberOfNestedElements()):
      parameterSetXml = elastixParameterSetDatabaseXml.GetNestedElement(parameterSetIndex)
      parameterFilesXml = parameterSetXml.FindNestedElementWithName('ParameterFiles')
      parameterFiles = []
      for parameterFileIndex in range(parameterFilesXml.GetNumberOfNestedElements()):
        parameterFiles.append(parameterFilesXml.GetNestedElement(parameterFileIndex).GetAttribute('Name'))
      parameterSetAttributes = \
        [parameterSetXml.GetAttribute(attr) for attr in ['id', 'modality', 'content', 'description', 'publications']]
      self.registrationPresets.append(parameterSetAttributes + [parameterFiles])
    return self.registrationPresets

  def getRegistrationIndexByPresetId(self, presetId):
    for presetIndex, preset in enumerate(self.getRegistrationPresets()):
      if preset[RegistrationPresets_Id] == presetId:
        return presetIndex
    message = f"Registration preset with id '{presetId}' could not be found.  Falling back to default preset."
    logging.warning(message)
    self.addLog(message)
    return 0

  def startElastix(self, cmdLineArguments):
    self.addLog("Register volumes...")
    executableFilePath = os.path.join(self.getElastixBinDir(), self.elastixFilename)
    logging.info(f"Register volumes using: {executableFilePath}: {cmdLineArguments!r}")
    return self._createSubProcess(executableFilePath, cmdLineArguments)

  def startTransformix(self, cmdLineArguments):
    self.addLog("Generate output...")
    executableFilePath = os.path.join(self.getElastixBinDir(), self.transformixFilename)
    logging.info(f"Generate output using: {executableFilePath}: {cmdLineArguments!r}")
    return self._createSubProcess(executableFilePath, cmdLineArguments)

  def _createSubProcess(self, executableFilePath, cmdLineArguments):
    return subprocess.Popen([executableFilePath] + cmdLineArguments, env=self.getElastixEnv(),
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,
                            startupinfo=self.getStartupInfo())

  def getStartupInfo(self):
    import platform
    if platform.system() != 'Windows':
      return None

    # Hide console window (only needed on Windows)
    import subprocess
    info = subprocess.STARTUPINFO()
    info.dwFlags = 1
    info.wShowWindow = 0
    return info

  def logProcessOutput(self, process):
    # save process output (if not logged) so that it can be displayed in case of an error
    processOutput = ''
    import subprocess

    while True:
      try:
        stdout_line = process.stdout.readline()
        if not stdout_line:
          break
        stdout_line = stdout_line.rstrip()
        if self.logStandardOutput:
          self.addLog(stdout_line)
        else:
          processOutput += stdout_line + '\n'
      except UnicodeDecodeError as e:
        # Probably system locale is set to non-English, we cannot easily capture process output.
        # Code page conversion happens because `universal_newlines=True` sets process output to text mode.
        pass
      slicer.app.processEvents()  # give a chance to click Cancel button
      if self.cancelRequested:
        process.kill()
        break

    process.stdout.close()
    return_code = process.wait()
    if return_code and not self.cancelRequested:
      if processOutput:
        self.addLog(processOutput)
      raise subprocess.CalledProcessError(return_code, "elastix")

  def createTempDirectory(self):
    tempDir = qt.QDir(self.getTempDirectoryBase())
    tempDirName = qt.QDateTime().currentDateTime().toString("yyyyMMdd_hhmmss_zzz")
    fileInfo = qt.QFileInfo(qt.QDir(tempDir), tempDirName)
    return self.createDirectory(fileInfo.absoluteFilePath())

  def getTempDirectoryBase(self):
    tempDir = qt.QDir(slicer.app.temporaryPath)
    fileInfo = qt.QFileInfo(qt.QDir(tempDir), "Elastix")
    return self.createDirectory(fileInfo.absoluteFilePath())

  def registerVolumesUsingParameterNode(self, parameterNode):
    presetId = parameterNode.GetParameter(self.REGISTRATION_PRESET_ID_PARAM)
    presetIdx = self.getRegistrationIndexByPresetId(presetId)
    registrationPreset = self.getRegistrationPresets()[presetIdx]
    parameterFilenames = registrationPreset[RegistrationPresets_ParameterFilenames]

    self.registerVolumes(
      fixedVolumeNode=parameterNode.GetNodeReference(self.FIXED_VOLUME_REF),
      movingVolumeNode=parameterNode.GetNodeReference(self.MOVING_VOLUME_REF),
      parameterFilenames=parameterFilenames,
      outputVolumeNode=parameterNode.GetNodeReference(self.OUTPUT_VOLUME_REF),
      outputTransformNode=parameterNode.GetNodeReference(self.OUTPUT_TRANSFORM_REF),
      fixedVolumeMaskNode=parameterNode.GetNodeReference(self.FIXED_VOLUME_MASK_REF),
      movingVolumeMaskNode=parameterNode.GetNodeReference(self.MOVING_VOLUME_MASK_REF),
      forceDisplacementFieldOutputTransform=slicer.util.toBool(parameterNode.GetParameter(self.FORCE_GRID_TRANSFORM_PARAM)),
      initialTransformNode=parameterNode.GetNodeReference(self.INITIAL_TRANSFORM_REF))

  def registerVolumes(self, fixedVolumeNode, movingVolumeNode, parameterFilenames=None, outputVolumeNode=None,
                      outputTransformNode=None, fixedVolumeMaskNode=None, movingVolumeMaskNode=None,
                      forceDisplacementFieldOutputTransform=True, initialTransformNode=None):

    self.isRunning = True
    try:
      if parameterFilenames is None:
        self.addLog(f"Using default registration preset with id '{self.DEFAULT_PRESET_ID}'")
        defaultPresetIndex = self.getRegistrationIndexByPresetId(self.DEFAULT_PRESET_ID)
        parameterFilenames = self.getRegistrationPresets()[defaultPresetIndex][RegistrationPresets_ParameterFilenames]

      self.cancelRequested = False

      tempDir = self.createTempDirectory()
      self.addLog(f'Volume registration is started in working directory: {tempDir}')

      # Specify (and create) input/output locations
      inputDir = self.createDirectory(os.path.join(tempDir, self.INPUT_DIR_NAME))
      resultTransformDir = self.createDirectory(os.path.join(tempDir, self.OUTPUT_TRANSFORM_DIR_NAME))

      # compose parameters for running Elastix
      inputParamsElastix = self._addInputVolumes(inputDir, [
        [fixedVolumeNode, 'fixed.mha', '-f'],
        [movingVolumeNode, 'moving.mha', '-m'],
        [fixedVolumeMaskNode, 'fixedMask.mha', '-fMask'],
        [movingVolumeMaskNode, 'movingMask.mha', '-mMask']
      ])

      if initialTransformNode is not None:
        inputParamsElastix += self._addInitialTransform(initialTransformNode, inputDir)

      inputParamsElastix += self._addParameterFiles(parameterFilenames)
      inputParamsElastix += ['-out', resultTransformDir]

      elastixProcess = self.startElastix(inputParamsElastix)
      self.logProcessOutput(elastixProcess)

      if self.cancelRequested:
        self.addLog("User requested cancel.")
      else:
        self._processElastixOutput(tempDir, parameterFilenames, fixedVolumeNode, movingVolumeNode,
                                   outputVolumeNode, outputTransformNode, forceDisplacementFieldOutputTransform)
        self.addLog("Registration is completed")

    finally: # Clean up
      if self.deleteTemporaryFiles:
        import shutil
        shutil.rmtree(tempDir)
      self.isRunning = False
      self.cancelRequested = False

  def _processElastixOutput(self, tempDir, parameterFilenames, fixedVolumeNode, movingVolumeNode, outputVolumeNode,
                            outputTransformNode, forceDisplacementFieldOutputTransform):

    resultTransformDir = os.path.join(tempDir, self.OUTPUT_TRANSFORM_DIR_NAME)
    transformFileNameBase = os.path.join(resultTransformDir, 'TransformParameters.' + str(len(parameterFilenames) - 1))

    # Load Linear Transform if available
    elastixTransformFileImported = False
    if outputTransformNode is not None and not forceDisplacementFieldOutputTransform:
      # NB: if return value is False, Could not load transform (probably not linear and bspline)
      try:
        self.loadTransformFromFile(f"{transformFileNameBase}-Composite.h5", outputTransformNode)
        elastixTransformFileImported = True
      except:
        elastixTransformFileImported = False

    resultResampleDir = self.createDirectory(os.path.join(tempDir, self.OUTPUT_RESAMPLE_DIR_NAME))
    # Run Transformix to get resampled moving volume or transformation as a displacement field
    if outputVolumeNode is not None or not elastixTransformFileImported:
      inputParamsTransformix = [
        '-tp', f'{transformFileNameBase}.txt',
        '-out', resultResampleDir
      ]
      if outputVolumeNode:
        inputDir = os.path.join(tempDir, self.INPUT_DIR_NAME)
        inputParamsTransformix += ['-in', os.path.join(inputDir, 'moving.mha')]

      if outputTransformNode:
        inputParamsTransformix += ['-def', 'all']

      transformixProcess = self.startTransformix(inputParamsTransformix)
      self.logProcessOutput(transformixProcess)

    if outputVolumeNode:
      self._loadTransformedOutputVolume(outputVolumeNode, resultResampleDir)

    if outputTransformNode is not None and not elastixTransformFileImported:
      outputTransformPath = os.path.join(resultResampleDir, "deformationField.mhd")
      try:
        self.loadTransformFromFile(outputTransformPath, outputTransformNode)
      except:
        raise RuntimeError(f"Failed to load output transform from {outputTransformPath}")

      if slicer.app.majorVersion >= 5 or (slicer.app.majorVersion >= 4 and slicer.app.minorVersion >= 11):
        outputTransformNode.AddNodeReferenceID(
          slicer.vtkMRMLTransformNode.GetMovingNodeReferenceRole(), movingVolumeNode.GetID()
        )
        outputTransformNode.AddNodeReferenceID(
          slicer.vtkMRMLTransformNode.GetFixedNodeReferenceRole(), fixedVolumeNode.GetID()
        )

  def _loadTransformedOutputVolume(self, outputVolumeNode, resultResampleDir):
    outputVolumePath = os.path.join(resultResampleDir, "result.mhd")
    try:
      loadedOutputVolumeNode = slicer.util.loadVolume(outputVolumePath)
      outputVolumeNode.SetAndObserveImageData(loadedOutputVolumeNode.GetImageData())
      ijkToRas = vtk.vtkMatrix4x4()
      loadedOutputVolumeNode.GetIJKToRASMatrix(ijkToRas)
      outputVolumeNode.SetIJKToRASMatrix(ijkToRas)
      slicer.mrmlScene.RemoveNode(loadedOutputVolumeNode)
    except:
      raise RuntimeError(f"Failed to load output volume from {outputVolumePath}")

  def _addInputVolumes(self, inputDir, inputVolumes):
    params = []
    for volumeNode, filename, paramName in inputVolumes:
      if not volumeNode:
        continue
      filePath = os.path.join(inputDir, filename)
      slicer.util.exportNode(volumeNode, filePath)
      params += [paramName, filePath]
    return params

  def _addParameterFiles(self, parameterFilenames):
    params = []
    for parameterFilename in parameterFilenames:
      parameterFilePath = os.path.abspath(os.path.join(self.registrationParameterFilesDir, parameterFilename))
      params += ['-p', parameterFilePath]
    return params

  def _addInitialTransform(self, initialTransformNode, inputDir):
    # Save node
    initialTransformFile = os.path.join(inputDir, 'initialTransform.h5')
    slicer.util.exportNode(initialTransformNode, initialTransformFile)
    # Compose settings
    initialTransformParameterFile = os.path.join(inputDir, 'initialTransformParameter.txt')
    initialTransformSettings = [
      '(InitialTransformParametersFileName "NoInitialTransform")',
      '(HowToCombineTransforms "Compose")',
      '(Transform "File")',
      '(TransformFileName "%s")' % initialTransformFile,
      '\n'
    ]
    with open(initialTransformParameterFile, 'w') as f:
      f.write('\n'.join(initialTransformSettings))

    return ['-t0', initialTransformParameterFile]

  def createDirectory(self, path):
    if qt.QDir().mkpath(path):
      return path
    else:
      raise RuntimeError(f"Failed to create directory {path}")

  def loadTransformFromFile(self, fileName, node):
    tmpNode = slicer.util.loadTransform(fileName)
    node.CopyContent(tmpNode)
    slicer.mrmlScene.RemoveNode(tmpNode)

#
# Reg_Spine_prepostTest
#

class Reg_Spine_prepostTest(ScriptedLoadableModuleTest):
    """
    This is the test case for your scripted module.
    Uses ScriptedLoadableModuleTest base class, available at:
    https://github.com/Slicer/Slicer/blob/main/Base/Python/slicer/ScriptedLoadableModule.py
    """

    def setUp(self):
        """ Do whatever is needed to reset the state - typically a scene clear will be enough.
        """
        slicer.mrmlScene.Clear()

    def runTest(self):
        """Run as few or as many tests as needed here.
        """
        self.setUp()
        self.test_Reg_Spine_prepost1()

    def test_Reg_Spine_prepost1(self):
        """ Ideally you should have several levels of tests.  At the lowest level
        tests should exercise the functionality of the logic with different inputs
        (both valid and invalid).  At higher levels your tests should emulate the
        way the user would interact with your code and confirm that it still works
        the way you intended.
        One of the most important features of the tests is that it should alert other
        developers when their changes will have an impact on the behavior of your
        module.  For example, if a developer removes a feature that you depend on,
        your test should break so they know that the feature is needed.
        """

        self.delayDisplay("Starting the test")

        # Get/create input data

        import SampleData
        registerSampleData()
        inputVolume = SampleData.downloadSample('Reg_Spine_prepost1')
        self.delayDisplay('Loaded test data set')

        inputScalarRange = inputVolume.GetImageData().GetScalarRange()
        self.assertEqual(inputScalarRange[0], 0)
        self.assertEqual(inputScalarRange[1], 695)

        outputVolume = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLScalarVolumeNode")
        threshold = 100

        # Test the module logic

        logic = Reg_Spine_prepostLogic()

        # Test algorithm with non-inverted threshold
        logic.process(inputVolume, outputVolume, threshold, True)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], threshold)

        # Test algorithm with inverted threshold
        logic.process(inputVolume, outputVolume, threshold, False)
        outputScalarRange = outputVolume.GetImageData().GetScalarRange()
        self.assertEqual(outputScalarRange[0], inputScalarRange[0])
        self.assertEqual(outputScalarRange[1], inputScalarRange[1])

        self.delayDisplay('Test passed')


RegistrationPresets_Id = 0
RegistrationPresets_Modality = 1
RegistrationPresets_Content = 2
RegistrationPresets_Description = 3
RegistrationPresets_Publications = 4
RegistrationPresets_ParameterFilenames = 5