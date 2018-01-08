#!/usr/bin/env python
import os
import sys
import platform
import reportlab.lib.enums
import copy
import sys
sys.path.insert(0, '..')


from common.PluginManager import PluginManager
from common.NWProcContext import NWProcContext
from common.NWDocument import NWDocument

import common.utils_fs as cmn_utils_fs
import common.utils_di as cmn_utils_di
import common.utils_rp as cmn_utils_rp


class NWGenerator:
    def __init__(self, aSourcePath, aOutputPath, extPluginFolders=[]):
        self.pluginMng = PluginManager()

        self.pluginMng.addPluginFolder(
            os.path.join(os.path.dirname(__file__),
                         '../plugins/'))

        for extPluginFolder in extPluginFolders:
            self.pluginMng.addPluginFolder(extPluginFolder)

        self.pluginMng.loadPlugins()

        # Load general prefs
        docInfos = cmn_utils_fs.deserialize(
            os.path.join(aSourcePath,
                         "doc_info.yaml"))

        self.context = NWProcContext(docInfos,
                                     aSourcePath,
                                     aOutputPath,
                                     self.prepareBlocks,
                                     self.processBlocks)

        self.overrideValues(
            'styles', self.context.styleSheet, self.context.docInfo)

        self.doc = NWDocument(self.context.docInfo, self.context.styleSheet)
        self.context.doc = self.doc

    def overrideValues(self, strkey, dicTraget, dicSource):
        if strkey in dicSource:
            dicTraget.update(dicSource[strkey])

    def setStyleSheet(self, obj):
        self.context.styleSheet = obj
        self.overrideValues(
            'styles', self.context.styleSheet, self.context.docInfo)
        self.doc.setStyleSheet(obj)

    def addDecoration(self, funcObj):
        self.doc.addDecoration(funcObj)

    def prepareBlocks(self, blocks, context, path):
        for block in blocks:
            block['_path'] = path
            plugin = self.pluginMng.findPlugin(block['type'])
            if plugin is not None:
                plugin.prepare(block, context)
            else:
                print('Plugin not found: %s' % block['type'])

    def processBlocks(self, blocks, context, path):
        content = []
        for block in blocks:
            block['_path'] = path
            plugin = self.pluginMng.findPlugin(block['type'])
            if plugin is not None:
                content.extend(plugin.process(block, context))
            else:
                print('Plugin not found: %s' % block['type'])

        return content

    def process(self):
        blocks = []
        for block in self.processFolder(self.context.sourcePath):
            blocks.append(block)
        
        # prepare blocks
        for block in blocks:
            plugin = self.pluginMng.findPlugin(block['type'])
            if plugin is not None:
                plugin.prepare(block, self.context)
            else:
                print('Plugin not found: %s' % block['type'])

        # process blocks
        content = []
        content.append(cmn_utils_rp.TriggerFlowable(self.context.buildBegins))

        for block in blocks:
            plugin = self.pluginMng.findPlugin(block['type'])
            if plugin is not None:
                content.extend(plugin.process(block, self.context))
            else:
                print('Plugin not found: %s' % block['type'])

        content.extend(self.context.process())

        if not os.path.isdir(self.context.outputPath):
            os.makedirs(self.context.outputPath)

        outputfile = os.path.join(
            self.context.outputPath,
            self.context.docInfo["outputFileTemplate"])
        self.doc.build(outputfile, self.context, content)

        return self.context.pageCounter.pageCount

    def processFolder(self, path):
        for item in sorted(os.listdir(path)):
            itemPath = os.path.join(path, item)

            if os.path.isdir(itemPath) and not item.startswith("."):
                for subitem in self.processFolder(itemPath):
                    yield subitem
            elif item.endswith(".yaml"):
                parts = cmn_utils_fs.loadYAML(itemPath)

                if type(parts) is not list:
                    continue

                for part in parts:
                    if "type" not in part:
                        continue

                    # add file path for assets loading
                    part['_path'] = path

                    yield part
