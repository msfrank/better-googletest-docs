
SOURCE_DIR="content"
DOCS_DIR="content/googletest/docs"
REFS_DIR="content/googletest/docs/reference"
BUILD_ROOT="_build"
CONTENT_DIR="${BUILD_ROOT}/content"
OUTPUT_DIR="${BUILD_ROOT}/output"
BUILDER="html"

# remove the build root if it exists
rm -rf ${BUILD_ROOT}

# create the content directory
mkdir -p ${CONTENT_DIR}

# copy the .rst files from the source directory
cp ${SOURCE_DIR}/*.rst ${CONTENT_DIR}

# rewrite the .md files from the docs directory and write them to the content directory
for MDFILE in $(ls -1 ${DOCS_DIR}/*.md); do
  #cp ${MDFILE} ${CONTENT_DIR}/$(basename ${MDFILE})
  uv run rewrite_md.py ${MDFILE} -o ${CONTENT_DIR}/$(basename ${MDFILE})
done

# remove the index.md from googletest because it conflicts with the sphinx index.rst
rm -f ${CONTENT_DIR}/index.md

# rewrite the .md files from the docs directory and write them to the content directory
for MDFILE in $(ls -1 ${REFS_DIR}/*.md); do
  #cp ${MDFILE} ${CONTENT_DIR}/$(basename ${MDFILE})
  uv run rewrite_md.py ${MDFILE} -o ${CONTENT_DIR}/$(basename ${MDFILE})
done

# build the documentation
uv run sphinx-build --conf-dir . --write-all -b ${BUILDER} ${CONTENT_DIR} ${OUTPUT_DIR}/${BUILDER}
