# This file is part of concourse-lp-livefs-resource
#
# Copyright 2023 Canonical Ltd.
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License version 3, as published by
# the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranties of MERCHANTABILITY,
# SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

FROM ubuntu:jammy-20230816
RUN apt-get update && apt-get install -y python3 python3-requests python3-requests-oauthlib python3-launchpadlib
ADD /check /out /in /lputils.py /opt/resource/
RUN chmod +x /opt/resource/*
