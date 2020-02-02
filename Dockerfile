# (C) Copyright Banco do Brasil 2019.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
FROM atf.intranet.bb.com.br:5001/bb/lnx/lnx-python3-centos:3.6.8

ARG build_date
ARG vcs_ref
ARG VERSAO=0.1.1
ARG BOM_PATH="/docker/nia"

LABEL \
    br.com.bb.image.app.sigla="nia" \
    br.com.bb.image.app.provider="" \
    br.com.bb.image.app.arch="x86_64" \
    br.com.bb.image.app.maintainer="Banco do Brasil S.A. / DITEC <ditec@bb.com.br>" \
    br.com.bb.image.app.version="$VERSAO" \
    br.com.bb.image.description="" \
    org.label-schema.maintainer="Banco do Brasil S.A. / DITEC <ditec@bb.com.br>" \
    org.label-schema.vendor="Banco do Brasil" \
    org.label-schema.url="https://fontes.intranet.bb.com.br/nia/nia-sauron-spoofing-controller/nia-sauron-spoofing-controller" \
    org.label-schema.name="" \
    org.label-schema.license="COPYRIGHT" \
    org.label-schema.version="$VERSAO" \
    org.label-schema.vcs-url="https://fontes.intranet.bb.com.br/nia/nia-sauron-spoofing-controller/nia-sauron-spoofing-controller" \
    org.label-schema.vcs-ref="$vcs_ref" \
    org.label-schema.build-date="$build_date" \
    org.label-schema.schema-version="1.0" \
    org.label-schema.dockerfile="${BOM_PATH}/Dockerfile"

# Save Bill of Materials to image. Não remova!
COPY README.md CHANGELOG.md LICENSE Dockerfile ${BOM_PATH}/

ENV \
    VERSAO=$VERSAO

RUN mkdir -p /usr/src/app
COPY . /usr/src/app

RUN yum install -y gcc gcc-c++ make cmake python36-devel boost-devel libXext libSM libXrender

ENV CMAKE_C_COMPILER=/usr/bin/gcc CMAKE_CXX_COMPILER=/usr/bin/g++ MODE=prod

WORKDIR /usr/src/app/

RUN python3 -m pip install -U pip && pip install -e .

EXPOSE 9000

# Save Bill of Materials to image. Não remova!
COPY README.md CHANGELOG.md LICENSE Dockerfile ${BOM_PATH}/

WORKDIR /usr/src/app/nia_sauron_spoofing_controller/

# Run gunicorn
ENTRYPOINT ["gunicorn", "-c", "config/config.py", "main:app"]
