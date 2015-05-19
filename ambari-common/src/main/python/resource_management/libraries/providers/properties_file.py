#!/usr/bin/env python
"""
Licensed to the Apache Software Foundation (ASF) under one
or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.  The ASF licenses this file
to you under the Apache License, Version 2.0 (the
"License"); you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Ambari Agent

"""

import time
import os
import resource_management
from resource_management.core.resources import File
from resource_management.core.providers import Provider
from resource_management.core.source import InlineTemplate
from resource_management.libraries.functions.format import format
from resource_management.core.environment import Environment
from resource_management.core.logger import Logger


class PropertiesFileProvider(Provider):
  def action_create(self):
    filename = self.resource.filename
    dir = self.resource.dir
    if dir == None:
      filepath = filename
    else:
      filepath = os.path.join(dir, filename)

    config_content = InlineTemplate('''# Generated by Apache Ambari. {{time.asctime(time.localtime())}}
    {% for key, value in properties_dict|dictsort %}
{{key}}{{key_value_delimiter}}{{ resource_management.core.source.InlineTemplate(str(value)).get_content() }}{% endfor %}
    ''', extra_imports=[time, resource_management, resource_management.core, resource_management.core.source], properties_dict=self.resource.properties, key_value_delimiter=self.resource.key_value_delimiter)

    Logger.info(format("Generating properties file: {filepath}"))

    with Environment.get_instance_copy() as env:
      File (format("{filepath}"),
            content = config_content,
            owner = self.resource.owner,
            group = self.resource.group,
            mode = self.resource.mode
      )
