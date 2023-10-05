# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\Extensions\Spine_Registration\Reg_Spine_prepost\Reg_Spine_prepost\Resources\UI\Reg_Spine_prepost.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Elastix(object):
    def setupUi(self, Elastix):
        Elastix.setObjectName("Elastix")
        Elastix.resize(391, 796)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Elastix.sizePolicy().hasHeightForWidth())
        Elastix.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(Elastix)
        self.gridLayout.setObjectName("gridLayout")
        self.inputParametersCollapsibleButton = ctkCollapsibleButton(Elastix)
        self.inputParametersCollapsibleButton.setCollapsed(False)
        self.inputParametersCollapsibleButton.setObjectName("inputParametersCollapsibleButton")
        self.formLayout = QtWidgets.QFormLayout(self.inputParametersCollapsibleButton)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.inputParametersCollapsibleButton)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.fixedVolumeSelector = qMRMLNodeComboBox(self.inputParametersCollapsibleButton)
        self.fixedVolumeSelector.setEnabled(True)
        self.fixedVolumeSelector.setNodeTypes(['vtkMRMLScalarVolumeNode'])
        self.fixedVolumeSelector.setShowChildNodeTypes(False)
        self.fixedVolumeSelector.setHideChildNodeTypes([])
        self.fixedVolumeSelector.setBaseName("")
        self.fixedVolumeSelector.setNoneEnabled(False)
        self.fixedVolumeSelector.setAddEnabled(False)
        self.fixedVolumeSelector.setRemoveEnabled(False)
        self.fixedVolumeSelector.setRenameEnabled(True)
        self.fixedVolumeSelector.setInteractionNodeSingletonTag("")
        self.fixedVolumeSelector.setObjectName("fixedVolumeSelector")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fixedVolumeSelector)
        self.label_3 = QtWidgets.QLabel(self.inputParametersCollapsibleButton)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.movingVolumeSelector = qMRMLNodeComboBox(self.inputParametersCollapsibleButton)
        self.movingVolumeSelector.setEnabled(True)
        self.movingVolumeSelector.setNodeTypes(['vtkMRMLScalarVolumeNode'])
        self.movingVolumeSelector.setShowChildNodeTypes(False)
        self.movingVolumeSelector.setHideChildNodeTypes([])
        self.movingVolumeSelector.setBaseName("")
        self.movingVolumeSelector.setNoneEnabled(False)
        self.movingVolumeSelector.setAddEnabled(False)
        self.movingVolumeSelector.setRemoveEnabled(False)
        self.movingVolumeSelector.setRenameEnabled(True)
        self.movingVolumeSelector.setInteractionNodeSingletonTag("")
        self.movingVolumeSelector.setObjectName("movingVolumeSelector")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.movingVolumeSelector)
        self.registrationPresetSelector = QtWidgets.QComboBox(self.inputParametersCollapsibleButton)
        self.registrationPresetSelector.setObjectName("registrationPresetSelector")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.registrationPresetSelector)
        self.label_4 = QtWidgets.QLabel(self.inputParametersCollapsibleButton)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.gridLayout.addWidget(self.inputParametersCollapsibleButton, 2, 0, 1, 1)
        self.maskingParametersCollapsibleButton = ctkCollapsibleButton(Elastix)
        self.maskingParametersCollapsibleButton.setCollapsed(True)
        self.maskingParametersCollapsibleButton.setObjectName("maskingParametersCollapsibleButton")
        self.formLayout_4 = QtWidgets.QFormLayout(self.maskingParametersCollapsibleButton)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_5 = QtWidgets.QLabel(self.maskingParametersCollapsibleButton)
        self.label_5.setObjectName("label_5")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.fixedVolumeMaskSelector = qMRMLNodeComboBox(self.maskingParametersCollapsibleButton)
        self.fixedVolumeMaskSelector.setNodeTypes(['vtkMRMLLabelMapVolumeNode'])
        self.fixedVolumeMaskSelector.setShowChildNodeTypes(False)
        self.fixedVolumeMaskSelector.setHideChildNodeTypes([])
        self.fixedVolumeMaskSelector.setNoneEnabled(True)
        self.fixedVolumeMaskSelector.setAddEnabled(False)
        self.fixedVolumeMaskSelector.setRemoveEnabled(False)
        self.fixedVolumeMaskSelector.setInteractionNodeSingletonTag("")
        self.fixedVolumeMaskSelector.setSelectNodeUponCreation(True)
        self.fixedVolumeMaskSelector.setObjectName("fixedVolumeMaskSelector")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.fixedVolumeMaskSelector)
        self.label_6 = QtWidgets.QLabel(self.maskingParametersCollapsibleButton)
        self.label_6.setObjectName("label_6")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.movingVolumeMaskSelector = qMRMLNodeComboBox(self.maskingParametersCollapsibleButton)
        self.movingVolumeMaskSelector.setNodeTypes(['vtkMRMLLabelMapVolumeNode'])
        self.movingVolumeMaskSelector.setShowChildNodeTypes(False)
        self.movingVolumeMaskSelector.setHideChildNodeTypes([])
        self.movingVolumeMaskSelector.setNoneEnabled(True)
        self.movingVolumeMaskSelector.setAddEnabled(False)
        self.movingVolumeMaskSelector.setRemoveEnabled(False)
        self.movingVolumeMaskSelector.setInteractionNodeSingletonTag("")
        self.movingVolumeMaskSelector.setObjectName("movingVolumeMaskSelector")
        self.formLayout_4.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.movingVolumeMaskSelector)
        self.gridLayout.addWidget(self.maskingParametersCollapsibleButton, 3, 0, 1, 1)
        self.outputParametersCollapsibleButton = ctkCollapsibleButton(Elastix)
        self.outputParametersCollapsibleButton.setObjectName("outputParametersCollapsibleButton")
        self.formLayout_5 = QtWidgets.QFormLayout(self.outputParametersCollapsibleButton)
        self.formLayout_5.setObjectName("formLayout_5")
        self.label_7 = QtWidgets.QLabel(self.outputParametersCollapsibleButton)
        self.label_7.setObjectName("label_7")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.label_8 = QtWidgets.QLabel(self.outputParametersCollapsibleButton)
        self.label_8.setObjectName("label_8")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.outputVolumeSelector = qMRMLNodeComboBox(self.outputParametersCollapsibleButton)
        self.outputVolumeSelector.setNodeTypes(['vtkMRMLScalarVolumeNode'])
        self.outputVolumeSelector.setShowChildNodeTypes(False)
        self.outputVolumeSelector.setHideChildNodeTypes([])
        self.outputVolumeSelector.setNoneEnabled(True)
        self.outputVolumeSelector.setRenameEnabled(True)
        self.outputVolumeSelector.setInteractionNodeSingletonTag("")
        self.outputVolumeSelector.setObjectName("outputVolumeSelector")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.outputVolumeSelector)
        self.outputTransformSelector = qMRMLNodeComboBox(self.outputParametersCollapsibleButton)
        self.outputTransformSelector.setNodeTypes(['vtkMRMLTransformNode'])
        self.outputTransformSelector.setHideChildNodeTypes([])
        self.outputTransformSelector.setNoneEnabled(True)
        self.outputTransformSelector.setRenameEnabled(True)
        self.outputTransformSelector.setInteractionNodeSingletonTag("")
        self.outputTransformSelector.setObjectName("outputTransformSelector")
        self.formLayout_5.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.outputTransformSelector)
        self.gridLayout.addWidget(self.outputParametersCollapsibleButton, 4, 0, 1, 1)
        self.advancedCollapsibleButton = ctkCollapsibleButton(Elastix)
        self.advancedCollapsibleButton.setCollapsed(True)
        self.advancedCollapsibleButton.setObjectName("advancedCollapsibleButton")
        self.formLayout_2 = QtWidgets.QFormLayout(self.advancedCollapsibleButton)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_13 = QtWidgets.QLabel(self.advancedCollapsibleButton)
        self.label_13.setObjectName("label_13")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_13)
        self.forceDisplacementFieldOutputCheckbox = QtWidgets.QCheckBox(self.advancedCollapsibleButton)
        self.forceDisplacementFieldOutputCheckbox.setText("")
        self.forceDisplacementFieldOutputCheckbox.setObjectName("forceDisplacementFieldOutputCheckbox")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.forceDisplacementFieldOutputCheckbox)
        self.label_9 = QtWidgets.QLabel(self.advancedCollapsibleButton)
        self.label_9.setObjectName("label_9")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.showDetailedLogDuringExecutionCheckBox = QtWidgets.QCheckBox(self.advancedCollapsibleButton)
        self.showDetailedLogDuringExecutionCheckBox.setText("")
        self.showDetailedLogDuringExecutionCheckBox.setObjectName("showDetailedLogDuringExecutionCheckBox")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.showDetailedLogDuringExecutionCheckBox)
        self.label_10 = QtWidgets.QLabel(self.advancedCollapsibleButton)
        self.label_10.setObjectName("label_10")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.frame = QtWidgets.QFrame(self.advancedCollapsibleButton)
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.keepTemporaryFilesCheckBox = QtWidgets.QCheckBox(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.keepTemporaryFilesCheckBox.sizePolicy().hasHeightForWidth())
        self.keepTemporaryFilesCheckBox.setSizePolicy(sizePolicy)
        self.keepTemporaryFilesCheckBox.setText("")
        self.keepTemporaryFilesCheckBox.setObjectName("keepTemporaryFilesCheckBox")
        self.horizontalLayout.addWidget(self.keepTemporaryFilesCheckBox)
        self.showTemporaryFilesFolderButton = QtWidgets.QPushButton(self.frame)
        self.showTemporaryFilesFolderButton.setObjectName("showTemporaryFilesFolderButton")
        self.horizontalLayout.addWidget(self.showTemporaryFilesFolderButton)
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.frame)
        self.label_12 = QtWidgets.QLabel(self.advancedCollapsibleButton)
        self.label_12.setObjectName("label_12")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_12)
        self.showRegistrationParametersDatabaseFolderButton = QtWidgets.QPushButton(self.advancedCollapsibleButton)
        self.showRegistrationParametersDatabaseFolderButton.setObjectName("showRegistrationParametersDatabaseFolderButton")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.showRegistrationParametersDatabaseFolderButton)
        self.label_11 = QtWidgets.QLabel(self.advancedCollapsibleButton)
        self.label_11.setObjectName("label_11")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.customElastixBinDirSelector = ctkPathLineEdit(self.advancedCollapsibleButton)
        self.customElastixBinDirSelector.setObjectName("customElastixBinDirSelector")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.customElastixBinDirSelector)
        self.label_14 = QtWidgets.QLabel(self.advancedCollapsibleButton)
        self.label_14.setObjectName("label_14")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_14)
        self.initialTransformSelector = qMRMLNodeComboBox(self.advancedCollapsibleButton)
        self.initialTransformSelector.setNodeTypes(['vtkMRMLTransformNode', 'vtkMRMLLinearTransformNode'])
        self.initialTransformSelector.setShowChildNodeTypes(False)
        self.initialTransformSelector.setHideChildNodeTypes([])
        self.initialTransformSelector.setNoneEnabled(True)
        self.initialTransformSelector.setAddEnabled(False)
        self.initialTransformSelector.setInteractionNodeSingletonTag("")
        self.initialTransformSelector.setSelectNodeUponCreation(True)
        self.initialTransformSelector.setObjectName("initialTransformSelector")
        self.formLayout_2.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.initialTransformSelector)
        self.gridLayout.addWidget(self.advancedCollapsibleButton, 5, 0, 1, 1)
        self.inputParametersCollapsibleButton_2 = ctkCollapsibleButton(Elastix)
        self.inputParametersCollapsibleButton_2.setCollapsed(False)
        self.inputParametersCollapsibleButton_2.setObjectName("inputParametersCollapsibleButton_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.inputParametersCollapsibleButton_2)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_2 = QtWidgets.QFrame(self.inputParametersCollapsibleButton_2)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_16 = QtWidgets.QLabel(self.frame_2)
        self.label_16.setMaximumSize(QtCore.QSize(100, 16777215))
        self.label_16.setObjectName("label_16")
        self.gridLayout_2.addWidget(self.label_16, 0, 0, 1, 1)
        self.spineCT_prepost_selector = qMRMLNodeComboBox(self.frame_2)
        self.spineCT_prepost_selector.setEnabled(True)
        self.spineCT_prepost_selector.setMinimumSize(QtCore.QSize(0, 0))
        self.spineCT_prepost_selector.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.spineCT_prepost_selector.setNodeTypes(['vtkMRMLScalarVolumeNode'])
        self.spineCT_prepost_selector.setShowChildNodeTypes(True)
        self.spineCT_prepost_selector.setHideChildNodeTypes([])
        self.spineCT_prepost_selector.setBaseName("")
        self.spineCT_prepost_selector.setNoneEnabled(False)
        self.spineCT_prepost_selector.setAddEnabled(True)
        self.spineCT_prepost_selector.setRemoveEnabled(True)
        self.spineCT_prepost_selector.setEditEnabled(True)
        self.spineCT_prepost_selector.setRenameEnabled(True)
        self.spineCT_prepost_selector.setInteractionNodeSingletonTag("")
        self.spineCT_prepost_selector.setObjectName("spineCT_prepost_selector")
        self.gridLayout_2.addWidget(self.spineCT_prepost_selector, 0, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.pushButtonInitialSegSpine = QtWidgets.QPushButton(self.inputParametersCollapsibleButton_2)
        self.pushButtonInitialSegSpine.setEnabled(False)
        self.pushButtonInitialSegSpine.setMinimumSize(QtCore.QSize(200, 25))
        self.pushButtonInitialSegSpine.setMaximumSize(QtCore.QSize(200, 16777215))
        self.pushButtonInitialSegSpine.setObjectName("pushButtonInitialSegSpine")
        self.verticalLayout_2.addWidget(self.pushButtonInitialSegSpine, 0, QtCore.Qt.AlignHCenter)
        self.frame_6 = QtWidgets.QFrame(self.inputParametersCollapsibleButton_2)
        self.frame_6.setMinimumSize(QtCore.QSize(0, 180))
        self.frame_6.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_3 = QtWidgets.QFrame(self.frame_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.checkBox_vertebrae_T12 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_vertebrae_T12.setObjectName("checkBox_vertebrae_T12")
        self.gridLayout_3.addWidget(self.checkBox_vertebrae_T12, 2, 5, 1, 1)
        self.checkBox_vertebrae_L5 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_vertebrae_L5.setObjectName("checkBox_vertebrae_L5")
        self.gridLayout_3.addWidget(self.checkBox_vertebrae_L5, 3, 4, 1, 1)
        self.checkBox_vertebrae_T7 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_vertebrae_T7.setObjectName("checkBox_vertebrae_T7")
        self.gridLayout_3.addWidget(self.checkBox_vertebrae_T7, 2, 0, 1, 1)
        self.checkBox_vertebrae_L1 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_vertebrae_L1.setObjectName("checkBox_vertebrae_L1")
        self.gridLayout_3.addWidget(self.checkBox_vertebrae_L1, 3, 0, 1, 1)
        self.checkBox_vertebrae_T9 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_vertebrae_T9.setObjectName("checkBox_vertebrae_T9")
        self.gridLayout_3.addWidget(self.checkBox_vertebrae_T9, 2, 2, 1, 1)
        self.checkBox_vertebrae_T11 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_vertebrae_T11.setObjectName("checkBox_vertebrae_T11")
        self.gridLayout_3.addWidget(self.checkBox_vertebrae_T11, 2, 4, 1, 1)
        self.checkBox_vertebrae_T4 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_vertebrae_T4.setMinimumSize(QtCore.QSize(20, 0))
        self.checkBox_vertebrae_T4.setMaximumSize(QtCore.QSize(50, 16777215))
        self.checkBox_vertebrae_T4.setObjectName("checkBox_vertebrae_T4")
        self.gridLayout_3.addWidget(self.checkBox_vertebrae_T4, 1, 3, 1, 1)
        self.checkBox_vertebrae_L2 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_vertebrae_L2.setObjectName("checkBox_vertebrae_L2")
        self.gridLayout_3.addWidget(self.checkBox_vertebrae_L2, 3, 1, 1, 1)
        self.checkBox_vertebrae_T2 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_vertebrae_T2.setObjectName("checkBox_vertebrae_T2")
        self.gridLayout_3.addWidget(self.checkBox_vertebrae_T2, 1, 1, 1, 1)
        self.checkBox_vertebrae_T5 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_vertebrae_T5.setObjectName("checkBox_vertebrae_T5")
        self.gridLayout_3.addWidget(self.checkBox_vertebrae_T5, 1, 4, 1, 1)
        self.checkBox_vertebrae_T6 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_vertebrae_T6.setObjectName("checkBox_vertebrae_T6")
        self.gridLayout_3.addWidget(self.checkBox_vertebrae_T6, 1, 5, 1, 1)
        self.checkBox_vertebrae_T8 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_vertebrae_T8.setObjectName("checkBox_vertebrae_T8")
        self.gridLayout_3.addWidget(self.checkBox_vertebrae_T8, 2, 1, 1, 1)
        self.checkBox_vertebrae_T10 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_vertebrae_T10.setObjectName("checkBox_vertebrae_T10")
        self.gridLayout_3.addWidget(self.checkBox_vertebrae_T10, 2, 3, 1, 1)
        self.checkBox_vertebrae_L3 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_vertebrae_L3.setObjectName("checkBox_vertebrae_L3")
        self.gridLayout_3.addWidget(self.checkBox_vertebrae_L3, 3, 2, 1, 1)
        self.checkBox_vertebrae_L4 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_vertebrae_L4.setObjectName("checkBox_vertebrae_L4")
        self.gridLayout_3.addWidget(self.checkBox_vertebrae_L4, 3, 3, 1, 1)
        self.checkBox_vertebrae_T1 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_vertebrae_T1.setMinimumSize(QtCore.QSize(20, 0))
        self.checkBox_vertebrae_T1.setMaximumSize(QtCore.QSize(50, 16777215))
        self.checkBox_vertebrae_T1.setObjectName("checkBox_vertebrae_T1")
        self.gridLayout_3.addWidget(self.checkBox_vertebrae_T1, 1, 0, 1, 1)
        self.checkBox_vertebrae_T3 = QtWidgets.QCheckBox(self.frame_3)
        self.checkBox_vertebrae_T3.setObjectName("checkBox_vertebrae_T3")
        self.gridLayout_3.addWidget(self.checkBox_vertebrae_T3, 1, 2, 1, 1)
        self.verticalLayout.addWidget(self.frame_3, 0, QtCore.Qt.AlignHCenter)
        self.frame_5 = QtWidgets.QFrame(self.frame_6)
        self.frame_5.setMinimumSize(QtCore.QSize(0, 60))
        self.frame_5.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.frame_4 = QtWidgets.QFrame(self.frame_5)
        self.frame_4.setMinimumSize(QtCore.QSize(100, 60))
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_15 = QtWidgets.QLabel(self.frame_4)
        self.label_15.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_15.setObjectName("label_15")
        self.gridLayout_4.addWidget(self.label_15, 0, 0, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.frame_4)
        self.label_17.setMaximumSize(QtCore.QSize(80, 16777215))
        self.label_17.setObjectName("label_17")
        self.gridLayout_4.addWidget(self.label_17, 1, 0, 1, 1)
        self.spineCT_pre_selector = qMRMLNodeComboBox(self.frame_4)
        self.spineCT_pre_selector.setEnabled(True)
        self.spineCT_pre_selector.setMinimumSize(QtCore.QSize(0, 0))
        self.spineCT_pre_selector.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.spineCT_pre_selector.setNodeTypes(['vtkMRMLScalarVolumeNode'])
        self.spineCT_pre_selector.setShowChildNodeTypes(True)
        self.spineCT_pre_selector.setHideChildNodeTypes([])
        self.spineCT_pre_selector.setBaseName("")
        self.spineCT_pre_selector.setNoneEnabled(False)
        self.spineCT_pre_selector.setAddEnabled(True)
        self.spineCT_pre_selector.setRemoveEnabled(True)
        self.spineCT_pre_selector.setEditEnabled(True)
        self.spineCT_pre_selector.setRenameEnabled(True)
        self.spineCT_pre_selector.setInteractionNodeSingletonTag("")
        self.spineCT_pre_selector.setObjectName("spineCT_pre_selector")
        self.gridLayout_4.addWidget(self.spineCT_pre_selector, 0, 1, 1, 1)
        self.spineCT_post_selector = qMRMLNodeComboBox(self.frame_4)
        self.spineCT_post_selector.setEnabled(True)
        self.spineCT_post_selector.setMinimumSize(QtCore.QSize(0, 0))
        self.spineCT_post_selector.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.spineCT_post_selector.setNodeTypes(['vtkMRMLScalarVolumeNode'])
        self.spineCT_post_selector.setShowChildNodeTypes(True)
        self.spineCT_post_selector.setHideChildNodeTypes([])
        self.spineCT_post_selector.setBaseName("")
        self.spineCT_post_selector.setNoneEnabled(False)
        self.spineCT_post_selector.setAddEnabled(True)
        self.spineCT_post_selector.setRemoveEnabled(True)
        self.spineCT_post_selector.setEditEnabled(True)
        self.spineCT_post_selector.setRenameEnabled(True)
        self.spineCT_post_selector.setInteractionNodeSingletonTag("")
        self.spineCT_post_selector.setObjectName("spineCT_post_selector")
        self.gridLayout_4.addWidget(self.spineCT_post_selector, 1, 1, 1, 1)
        self.horizontalLayout_2.addWidget(self.frame_4)
        self.pushButtonCropVertebrae = QtWidgets.QPushButton(self.frame_5)
        self.pushButtonCropVertebrae.setEnabled(False)
        self.pushButtonCropVertebrae.setMinimumSize(QtCore.QSize(50, 40))
        self.pushButtonCropVertebrae.setMaximumSize(QtCore.QSize(90, 16777215))
        self.pushButtonCropVertebrae.setObjectName("pushButtonCropVertebrae")
        self.horizontalLayout_2.addWidget(self.pushButtonCropVertebrae)
        self.verticalLayout.addWidget(self.frame_5)
        self.verticalLayout_2.addWidget(self.frame_6)
        self.gridLayout.addWidget(self.inputParametersCollapsibleButton_2, 0, 0, 1, 1)
        self.parametersCollapsibleButton_2 = ctkCollapsibleButton(Elastix)
        self.parametersCollapsibleButton_2.setCollapsed(False)
        self.parametersCollapsibleButton_2.setObjectName("parametersCollapsibleButton_2")
        self.formLayout_3 = QtWidgets.QFormLayout(self.parametersCollapsibleButton_2)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label = QtWidgets.QLabel(self.parametersCollapsibleButton_2)
        self.label.setObjectName("label")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.parameterNodeSelector = qMRMLNodeComboBox(self.parametersCollapsibleButton_2)
        self.parameterNodeSelector.setNodeTypes(['vtkMRMLScriptedModuleNode'])
        self.parameterNodeSelector.setShowHidden(True)
        self.parameterNodeSelector.setHideChildNodeTypes([])
        self.parameterNodeSelector.setRenameEnabled(True)
        self.parameterNodeSelector.setInteractionNodeSingletonTag("")
        self.parameterNodeSelector.setObjectName("parameterNodeSelector")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.parameterNodeSelector)
        self.gridLayout.addWidget(self.parametersCollapsibleButton_2, 1, 0, 1, 1)
        self.statusLabel = QtWidgets.QPlainTextEdit(Elastix)
        self.statusLabel.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.statusLabel.setCenterOnScroll(True)
        self.statusLabel.setObjectName("statusLabel")
        self.gridLayout.addWidget(self.statusLabel, 7, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 8, 0, 1, 1)
        self.applyButton = QtWidgets.QPushButton(Elastix)
        self.applyButton.setEnabled(False)
        self.applyButton.setStyleSheet("QPushButton {\n"
"    font: 16px;\n"
"}")
        self.applyButton.setAutoDefault(True)
        self.applyButton.setDefault(True)
        self.applyButton.setObjectName("applyButton")
        self.gridLayout.addWidget(self.applyButton, 6, 0, 1, 1)

        self.retranslateUi(Elastix)
        Elastix.mrmlSceneChanged['vtkMRMLScene*'].connect(self.fixedVolumeSelector.setMRMLScene)
        Elastix.mrmlSceneChanged['vtkMRMLScene*'].connect(self.fixedVolumeMaskSelector.setMRMLScene)
        Elastix.mrmlSceneChanged['vtkMRMLScene*'].connect(self.movingVolumeMaskSelector.setMRMLScene)
        Elastix.mrmlSceneChanged['vtkMRMLScene*'].connect(self.movingVolumeSelector.setMRMLScene)
        Elastix.mrmlSceneChanged['vtkMRMLScene*'].connect(self.parameterNodeSelector.setMRMLScene)
        Elastix.mrmlSceneChanged['vtkMRMLScene*'].connect(self.outputTransformSelector.setMRMLScene)
        Elastix.mrmlSceneChanged['vtkMRMLScene*'].connect(self.outputVolumeSelector.setMRMLScene)
        Elastix.mrmlSceneChanged['vtkMRMLScene*'].connect(self.initialTransformSelector.setMRMLScene)
        Elastix.mrmlSceneChanged['vtkMRMLScene*'].connect(self.spineCT_prepost_selector.setMRMLScene)
        Elastix.mrmlSceneChanged['vtkMRMLScene*'].connect(self.spineCT_pre_selector.setMRMLScene)
        Elastix.mrmlSceneChanged['vtkMRMLScene*'].connect(self.spineCT_post_selector.setMRMLScene)
        QtCore.QMetaObject.connectSlotsByName(Elastix)

    def retranslateUi(self, Elastix):
        _translate = QtCore.QCoreApplication.translate
        self.inputParametersCollapsibleButton.setToolTip(_translate("Elastix", "Pick input volume sequence. Each time point will be registered to the fixed frame."))
        self.inputParametersCollapsibleButton.setText(_translate("Elastix", "Inputs (Pre-CT and Post-CT for registration)"))
        self.label_2.setText(_translate("Elastix", "Fixed volume (pre): "))
        self.fixedVolumeSelector.setToolTip(_translate("Elastix", "The moving volume will be transformed into this image space."))
        self.label_3.setText(_translate("Elastix", "Moving volume (post): "))
        self.movingVolumeSelector.setToolTip(_translate("Elastix", "This volume will be transformed into the fixed image space"))
        self.label_4.setText(_translate("Elastix", "Preset: "))
        self.maskingParametersCollapsibleButton.setText(_translate("Elastix", "Masking"))
        self.label_5.setText(_translate("Elastix", "Fixed volume mask (pre): "))
        self.fixedVolumeMaskSelector.setToolTip(_translate("Elastix", "Areas of the fixed volume where mask label is 0 will be ignored in the registration."))
        self.label_6.setText(_translate("Elastix", "Moving volume mask (post): "))
        self.movingVolumeMaskSelector.setToolTip(_translate("Elastix", "Areas of the moving volume where mask label is 0 will be ignored in the registration"))
        self.outputParametersCollapsibleButton.setText(_translate("Elastix", "Outputs"))
        self.label_7.setText(_translate("Elastix", "Output volume: "))
        self.label_8.setText(_translate("Elastix", "Output transform: "))
        self.outputVolumeSelector.setToolTip(_translate("Elastix", "(optional) The moving image warped to the fixed image space. NOTE: You must set at least one output object (transform and/or output volume)"))
        self.outputTransformSelector.setToolTip(_translate("Elastix", "(optional) Computed displacement field that transform nodes from moving volume space to fixed volume space. NOTE: You must set at least one output object (transform and/or output volume)."))
        self.advancedCollapsibleButton.setText(_translate("Elastix", "Advanced"))
        self.label_13.setText(_translate("Elastix", "Force grid output transform:"))
        self.forceDisplacementFieldOutputCheckbox.setToolTip(_translate("Elastix", "If this checkbox is checked then computed transform will be always returned as a grid transform (displacement field)."))
        self.label_9.setToolTip(_translate("Elastix", "Show detailed log during registration."))
        self.label_9.setText(_translate("Elastix", "Show detailed log during registration:"))
        self.showDetailedLogDuringExecutionCheckBox.setToolTip(_translate("Elastix", "Show detailed log during registration."))
        self.label_10.setToolTip(_translate("Elastix", "Keep temporary files (inputs, computed outputs, logs) after the registration is completed."))
        self.label_10.setText(_translate("Elastix", "Keep temporary files:"))
        self.keepTemporaryFilesCheckBox.setToolTip(_translate("Elastix", "Keep temporary files (inputs, computed outputs, logs) after the registration is completed."))
        self.showTemporaryFilesFolderButton.setToolTip(_translate("Elastix", "Open the folder where temporary files are stored."))
        self.showTemporaryFilesFolderButton.setText(_translate("Elastix", "Show temp folder"))
        self.label_12.setText(_translate("Elastix", "Registration presets:"))
        self.showRegistrationParametersDatabaseFolderButton.setToolTip(_translate("Elastix", "Open the folder where temporary files are stored."))
        self.showRegistrationParametersDatabaseFolderButton.setText(_translate("Elastix", "Show database folder"))
        self.label_11.setText(_translate("Elastix", "Custom Elastix toolbox location:"))
        self.customElastixBinDirSelector.setToolTip(_translate("Elastix", "Set bin directory of an Elastix installation (where elastix executable is located). \"\n"
"      \"If value is empty then default elastix (bundled with SlicerElastix extension) will be used."))
        self.label_14.setText(_translate("Elastix", "Initial transform: "))
        self.initialTransformSelector.setToolTip(_translate("Elastix", "Start the registration from the selected initial transform."))
        self.inputParametersCollapsibleButton_2.setToolTip(_translate("Elastix", "Pick input volume sequence. Each time point will be registered to the fixed frame."))
        self.inputParametersCollapsibleButton_2.setText(_translate("Elastix", "Preprocessing (Spine segmentation and vertebrae extraction)"))
        self.label_16.setText(_translate("Elastix", "Pre CT image:"))
        self.spineCT_prepost_selector.setToolTip(_translate("Elastix", "This volume will be transformed into the fixed image space"))
        self.pushButtonInitialSegSpine.setText(_translate("Elastix", "Initial Segment Spine"))
        self.checkBox_vertebrae_T12.setText(_translate("Elastix", "T12"))
        self.checkBox_vertebrae_L5.setText(_translate("Elastix", "L5"))
        self.checkBox_vertebrae_T7.setText(_translate("Elastix", "T7"))
        self.checkBox_vertebrae_L1.setText(_translate("Elastix", "L1"))
        self.checkBox_vertebrae_T9.setText(_translate("Elastix", "T9"))
        self.checkBox_vertebrae_T11.setText(_translate("Elastix", "T11"))
        self.checkBox_vertebrae_T4.setText(_translate("Elastix", "T4"))
        self.checkBox_vertebrae_L2.setText(_translate("Elastix", "L2"))
        self.checkBox_vertebrae_T2.setText(_translate("Elastix", "T2"))
        self.checkBox_vertebrae_T5.setText(_translate("Elastix", "T5"))
        self.checkBox_vertebrae_T6.setText(_translate("Elastix", "T6"))
        self.checkBox_vertebrae_T8.setText(_translate("Elastix", "T8"))
        self.checkBox_vertebrae_T10.setText(_translate("Elastix", "T10"))
        self.checkBox_vertebrae_L3.setText(_translate("Elastix", "L3"))
        self.checkBox_vertebrae_L4.setText(_translate("Elastix", "L4"))
        self.checkBox_vertebrae_T1.setText(_translate("Elastix", "T1"))
        self.checkBox_vertebrae_T3.setText(_translate("Elastix", "T3"))
        self.label_15.setText(_translate("Elastix", "Pre-CT:"))
        self.label_17.setText(_translate("Elastix", "Post-CT(aligned):"))
        self.spineCT_pre_selector.setToolTip(_translate("Elastix", "This volume will be transformed into the fixed image space"))
        self.spineCT_post_selector.setToolTip(_translate("Elastix", "This volume will be transformed into the fixed image space"))
        self.pushButtonCropVertebrae.setText(_translate("Elastix", "Crop Vertebrae"))
        self.parametersCollapsibleButton_2.setText(_translate("Elastix", "Parameter set"))
        self.label.setText(_translate("Elastix", "Parameter Set:"))
        self.parameterNodeSelector.setBaseName(_translate("Elastix", "ElastixParameters"))
        self.applyButton.setToolTip(_translate("Elastix", "Run the algorithm."))
        self.applyButton.setText(_translate("Elastix", "Apply"))

from ctkCollapsibleButton import ctkCollapsibleButton
from ctkPathLineEdit import ctkPathLineEdit
from qMRMLNodeComboBox import qMRMLNodeComboBox
from qMRMLWidget import qMRMLWidget