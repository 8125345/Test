import json

label = ['gjjj', '10mm', '8mm', '6mm', '5mm', '4mm', '3mm', '2mm', '1_5mm', 'dbl1', 'dbl2', 'dbl3', 'gj1', 'gj2',
             'gj3', 'st1', 'st2', 'st3']

label_xmm1 = ['10mm', '8mm', '6mm', '5mm', '4mm', '3mm']
label_xmm2 = ['2mm', '1_5mm']
label_dbl123 = ['dbl1', 'dbl2', 'dbl3']
label_gj123 = ['gj1', 'gj2', 'gj3']
label_st123 = ['st1', 'st2', 'st3']

with open('result.json', 'r', encoding='utf8') as fp:
    check_data = json.load(fp)

result =[]
for item in check_data:

    label_new = {'chen': {'date': 0, 'car_num': 0, 'gjjj': 0, 'Xmm1': 0, 'Xmm2': 0, 'dbl123': 0, 'gj123': 0, 'st123': 0},
                 'mask': {'date': 0, 'car_num': 0, 'gjjj': 0, 'Xmm1': 0, 'Xmm2': 0, 'dbl123': 0, 'gj123': 0, 'st123': 0}}
    sum_Xmm1_chen = 0
    sum_Xmm1_mask = 0
    sum_Xmm2_chen = 0
    sum_Xmm2_mask = 0
    sum_dbl123_chen = 0
    sum_dbl123_mask = 0
    sum_gj123_chen = 0
    sum_gj123_mask = 0
    sum_st123_chen = 0
    sum_st123_mask = 0
    # print(item)
    ch_data = item['chen']
    mask_data = item['mask']

    label_new['chen']['gjjj'] = ch_data['gjjj']
    label_new['mask']['gjjj'] = mask_data['gjjj']
    label_new['chen']['date'] = ch_data['date']
    label_new['mask']['date'] = mask_data['date']
    label_new['chen']['car_num'] = ch_data['car_num']
    label_new['mask']['car_num'] = mask_data['car_num']

    for k in label_xmm1:
        sum_Xmm1_chen += ch_data[k]
        sum_Xmm1_mask += mask_data[k]
    label_new['chen']['Xmm1'] = sum_Xmm1_chen
    label_new['mask']['Xmm1'] = sum_Xmm1_mask

    for k in label_xmm2:
        sum_Xmm2_chen += ch_data[k]
        sum_Xmm2_mask += mask_data[k]
    label_new['chen']['Xmm2'] = sum_Xmm2_chen
    label_new['mask']['Xmm2'] = sum_Xmm2_mask

    for k in label_dbl123:
        sum_dbl123_chen += ch_data[k]
        sum_dbl123_mask += mask_data[k]
    label_new['chen']['dbl123'] = sum_dbl123_chen
    label_new['mask']['dbl123'] = sum_dbl123_mask

    for k in label_gj123:
        sum_gj123_chen += ch_data[k]
        sum_gj123_mask += mask_data[k]
    label_new['chen']['gj123'] = sum_gj123_chen
    label_new['mask']['gj123'] = sum_gj123_mask


    for k in label_st123:
        sum_st123_chen += ch_data[k]
        sum_st123_mask += mask_data[k]
    label_new['chen']['st123'] = sum_st123_chen
    label_new['mask']['st123'] = sum_st123_mask

    result.append(label_new)

with open('result_combine_class.json', 'w', encoding='utf8') as fp:
    fp.write(json.dumps(result))




