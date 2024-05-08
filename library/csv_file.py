from ansible.module_utils.basic import AnsibleModule, missing_required_lib
import csv, traceback

from datetime import datetime


def generate_csv(module):
    try:
        windows_update_facts = module.params['windows_update_facts']
        result = dict()
        # Get the Today's day, month and year
        now = datetime.now()
        year_month_day_format = '%Y-%m-%d'
        dat = now.strftime(year_month_day_format)

        # length of keys in Hardware facts of each item
        windows_facts_length = 0
        windows_facts_key = []
        for hard_item in windows_update_facts:
            if isinstance(hard_item, dict):
                for _, value in hard_item.items():
                    for sub_item in value:
                        temp_len = len(list(sub_item.keys()))
                        if windows_facts_length <= temp_len:
                            windows_facts_length = temp_len
                            windows_facts_key = list(sub_item.keys())

        result['windows_keys'] = windows_facts_key

        hardware_facts_file_name = f'/tmp/windows-update-{dat}.csv'

        with open(hardware_facts_file_name, mode='w') as csv_file:
            # Hardware facts fieldnames
            writer = csv.DictWriter(csv_file, fieldnames=windows_facts_key)

            writer.writeheader()
            for windows_facts in windows_update_facts:
                for _, value in windows_facts.items():
                    if isinstance(value, list):
                        for hardware in value:
                            writer.writerow(hardware)
                        
        module.exit_json(**result)
    except Exception as e:
        module.fail_json(msg=traceback.format_exc())


def main():
    module = AnsibleModule(
        argument_spec=dict(
            windows_update_facts=dict(required=True, type='list'))
    )


    generate_csv(module)

if __name__ == "__main__":
    main()