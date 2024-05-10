from ansible.module_utils.basic import AnsibleModule, missing_required_lib
import csv, traceback

from datetime import datetime


def generate_csv(module):
    try:
        windows_update_facts = module.params['windows_update_facts']
        windows_hostname = module.params['windows_hostname']
        result = dict()
        # Get the Today's day, month and year
        now = datetime.now()
        year_month_day_format = '%Y-%m-%d'
        dat = now.strftime(year_month_day_format)

        # length of keys in Hardware facts of each item
        windows_facts_length = 0
        windows_facts_key = []
        found_update_count=windows_update_facts.get('windows_update_facts', 0)
        failed_update_count=windows_update_facts.get('failed_update_count', 0)
        installed_update_count=windows_update_facts.get('installed_update_count',0)
        windows_update_list = []
        for key, value in windows_update_facts.get('updates').items():
            if isinstance(value, dict):
                temp_dict = {}
                for key1, value1 in value.items():                    
                    if isinstance(value1,list) and 'kb'==key:
                        temp_dict.update({key1: "KB"+ value1})
                    elif isinstance(value1,list) and 'kb'!=key:
                        temp_dict.update({key1: " ,".join(value1)})
                    else:
                        temp_dict.update({key1: value1})
                    
                    if key1 not in windows_facts_key:
                        windows_facts_key.append(key1)
                temp_dict.update({'HOSTNAME': windows_hostname})
                windows_update_list.append(temp_dict)

        result['windows_update'] = windows_update_list
        result['windows_key'] =  windows_facts_key

        hardware_facts_file_name = f'/tmp/windows-update-{dat}.csv'

        with open(hardware_facts_file_name, mode='w') as csv_file:
            # Hardware facts fieldnames
            writer = csv.DictWriter(csv_file, fieldnames=windows_facts_key)
            writer.writeheader()
            for windows_facts in windows_update_list:
                writer.writerow(windows_facts)
        result['changed'] = True
                        
        module.exit_json(**result)
    except Exception as e:
        module.fail_json(msg=traceback.format_exc())


def main():
    module = AnsibleModule(
        argument_spec=dict(
            windows_hostname=dict(required=True, type='str'),
            windows_update_facts=dict(required=True, type='dict'))
    )


    generate_csv(module)

if __name__ == "__main__":
    main()
