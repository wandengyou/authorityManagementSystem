from pymaid.error import ErrorManager


CommonError = ErrorManager.create_manager('CommonError', 1000)
CommonError.add_error('NotExist', 1, 'query object does not exist')
CommonError.add_error('AnalyzeError', 2, 'json file resolution failed')
