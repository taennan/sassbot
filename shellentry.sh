#
#
#

sassbot()
{
    local root=${SASSBOT:-"."}
    python3.9 $root/cli $@
}
