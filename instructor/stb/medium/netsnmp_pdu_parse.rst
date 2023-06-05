.. Copyright 2022 National Technology & Engineering Solutions of Sandia, LLC
   (NTESS).  Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
   Government retains certain rights in this software.
   
   Redistribution and use in source and binary/rendered forms, with or without
   modification, are permitted provided that the following conditions are met:
   
    1. Redistributions of source code must retain the above copyright notice,
       this list of conditions and the following disclaimer.
    2. Redistributions in binary/rendered form must reproduce the above copyright
       notice, this list of conditions and the following disclaimer in the
       documentation and/or other materials provided with the distribution.
    3. Neither the name of the copyright holder nor the names of its contributors
       may be used to endorse or promote products derived from this software
       without specific prior written permission.
   
   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
   ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
   WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
   DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
   FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
   DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
   SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
   CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
   OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

.. _NetSNMP_PDU_parse:

NetSNMP PDU Parsing
===================

.. .. external

.. code-block:: c
   :linenos:

   typedef struct variable_list {
      /** NULL for last variable */
      struct variable_list *next_variable;    
      /** Object identifier of variable */
      oid            *name;   
      /** number of subid's in name */
      size_t          name_length;    
      /** ASN type of variable */
      u_char          type;   
      /** value of variable */
       netsnmp_vardata val;
      /** the length of the value to be copied into buf */
      size_t          val_len;
      /** buffer to hold the OID */
      oid             name_loc[MAX_OID_LEN];  
      /** 90 percentile < 40. */
      u_char          buf[40];
      /** (Opaque) hook for additional data */
      void           *data;
      /** callback to free above */
      void            (*dataFreeHook)(void *);    
      int             index;
   } netsnmp_variable_list;
   
.. code-block:: c
   :linenos:

   int snmp_pdu_parse(netsnmp_pdu *pdu, u_char * data, size_t * length){
      ...
    while ((int) *length > 0) {
        netsnmp_variable_list *vptemp;
        vptemp = (netsnmp_variable_list *) malloc(sizeof(*vptemp));
        if (NULL == vptemp) {
            return -1;
        }
        if (NULL == vp) {
            pdu->variables = vptemp;
        } else {
            vp->next_variable = vptemp;
        }
        vp = vptemp;

        vp->next_variable = NULL;
        vp->val.string = NULL;
        vp->name_length = MAX_OID_LEN;
        vp->name = NULL;
        vp->index = 0;
        vp->data = NULL;
        vp->dataFreeHook = NULL;

        data = snmp_parse_var_op(data, objid, &vp->name_length, &vp->type,
                                 &vp->val_len, &var_val, length);
        if (data == NULL)
            return -1;
        if (snmp_set_var_objid(vp, objid, vp->name_length))
            return -1;

        len = MAX_PACKET_LENGTH;
        DEBUGDUMPHEADER("recv", "Value");
        switch ((short) vp->type) {
        case ASN_INTEGER:
            vp->val.integer = (long *) vp->buf;
            vp->val_len = sizeof(long);
            asn_parse_int(var_val, &len, &vp->type,
                          (long *) vp->val.integer,
        ...



**Context**

 * ``data`` is attacker controlled

**Solution**

.. container:: toggle

 .. container:: toggle-header

    Show/Hide

 .. container:: toggle-body

    .. code-block:: c
       :linenos:
       :emphasize-lines: 27,29

       int snmp_pdu_parse(netsnmp_pdu *pdu, u_char * data, size_t * length){

        while ((int) *length > 0) {
            netsnmp_variable_list *vptemp;
            vptemp = (netsnmp_variable_list *) malloc(sizeof(*vptemp));
            if (NULL == vptemp) {
                return -1;
            }
            if (NULL == vp) {
                pdu->variables = vptemp;
            } else {
                vp->next_variable = vptemp;
            }
            vp = vptemp;

            vp->next_variable = NULL;
            vp->val.string = NULL;
            vp->name_length = MAX_OID_LEN;
            vp->name = NULL;
            vp->index = 0;
            vp->data = NULL;
            vp->dataFreeHook = NULL;

            data = snmp_parse_var_op(data, objid, &vp->name_length, &vp->type,
                                     &vp->val_len, &var_val, length);
            if (data == NULL)
                return -1;
            if (snmp_set_var_objid(vp, objid, vp->name_length))
                return -1;

            len = MAX_PACKET_LENGTH;
            DEBUGDUMPHEADER("recv", "Value");
            switch ((short) vp->type) {
            case ASN_INTEGER:
                vp->val.integer = (long *) vp->buf;
                vp->val_len = sizeof(long);
                asn_parse_int(var_val, &len, &vp->type,
                              (long *) vp->val.integer,
            ...


    The ``vptemp`` structure is only partially initialized after it is
    added to the ``pdu->variables`` list and so this function leaves the
    responsibility of cleaning up in the case of errors to the caller.  As it
    turns out, some paths don't handle this well and the incomplete variable ends
    up masquerading as a fully fledged member of the list causing downstream memory
    corruption issues.

    `Further Reading <https://sourceforge.net/p/net-snmp/bugs/2821/>`_
