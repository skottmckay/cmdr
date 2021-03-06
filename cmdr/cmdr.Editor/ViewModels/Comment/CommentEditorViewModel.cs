﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Linq;
using System.Windows.Input;
using cmdr.Editor.Utils;
using cmdr.WpfControls.DropDownButton;
using System.Collections.ObjectModel;
using System.Text.RegularExpressions;
using System.Globalization;

namespace cmdr.Editor.ViewModels.Comment
{
    public class CommentEditorViewModel : ViewModelBase
    {
        private readonly IEnumerable<MappingViewModel> _mappings;


        private ICommand _selectCommentsCommand;
        public ICommand SelectCommentsCommand
        {
            get { return _selectCommentsCommand ?? (_selectCommentsCommand = new CommandHandler<MenuItemViewModel>(selectComments)); }
        }

        private ICommand _sedCommentsCommand;
        public ICommand SedCommentsCommand
        {
            get
            {
                return _sedCommentsCommand ?? (_sedCommentsCommand = new CommandHandler(() => sedCommentsCommand()));
            }
        }

        private List<string> _selectedComments;
        private MenuItemViewModel _selectedCommentsMenuItem = new MenuItemViewModel { Text = "Selected Comments" };

        public ObservableCollection<MenuItemViewModel> CommentsMenu { get; private set; }

        private bool is_various;

        private string _comment;
        public string Comment
        {
            get { return _comment; }
            set
            {
                _comment = value;
                raisePropertyChanged("Comment");

                foreach (var mvm in _mappings)
                    mvm.Comment = _comment;

                updateCommentsMenu();
            }
        }


        private void selectComments(MenuItemViewModel item)
        {
            Comment = item.Tag.ToString();
        }


        public void sedCommentsDoSomething(SedResult sed)
        {

            foreach (var m in _mappings) {
                String cur = m.Comment;
                String new_st = cur;
                String search = (String)sed._search;
                String replace = (String)sed._replace;


                if (sed._oper == SedOperation.regular) {
                    // add whitespace, to remove later
                    if (sed.do_trim) {
                        new_st = String.Format(" {0} ", new_st);
                    }

                    if (search != "") {
                        new_st = new_st.Replace(search, replace);
                    }
                } else if (sed._oper == SedOperation.start) {
                    if (replace != "") {
                        new_st = replace + " " + new_st;
                    }
                } else if (sed._oper == SedOperation.end) {
                    if (replace != "") {
                        new_st = new_st + " " + replace;
                    }
                }

                if (sed._capitalize == SedCapitalize.none) {
                    // pass

                } else if (sed._capitalize == SedCapitalize.lowercase) {
                    new_st = new_st.ToLower();

                } else if (sed._capitalize == SedCapitalize.uppercase) {
                    new_st = new_st.ToUpper();

                } else if (sed._capitalize == SedCapitalize.titlecase) {
                    // https://stackoverflow.com/questions/1206019/converting-string-to-title-case
                    new_st = System.Threading.Thread.CurrentThread.CurrentCulture.TextInfo.
                                ToTitleCase(new_st.ToLower());
                    //new_st.ToTitleCase();
                }

                if (sed.do_trim) {
                    new_st = new_st.Trim();
                }
                m.Comment = new_st;
            }
        }

        // this opens the sed question window
        public void sedCommentsCommand()
        {
            SedResult sed = SedWindow.Prompt();
            if (sed != null) {
                sedCommentsDoSomething(sed);
            }

        }

        // automated search/replace
        public void sedCommentsReplaceString(String st_in, String st_out)
        {
            SedResult sed = new SedResult(st_in, st_out);
            sedCommentsDoSomething(sed);
        }

        public void sedCommentsReplaceDeck(int step)
        {
            Char ch_in = 'A'.Next(step - 1);
            Char ch_out = ch_in.Next(1);

            String st_in = String.Format(" {0} ", ch_in);
            String st_out = String.Format(" {0} ", ch_out);

            SedResult sed = new SedResult(st_in, st_out);
            sedCommentsDoSomething(sed);
        }

        public CommentEditorViewModel(IEnumerable<MappingViewModel> mappings)
        {
            _mappings = mappings;

            var common = _mappings.Select(m => m.Comment).Distinct();
            if (common.Count() == 1) {
                _comment = common.Single();
                is_various = false;
            } else if (common.Count() == 0) {
                _comment = String.Empty;
                is_various = false;
            } else {
                _comment = "<Various>";
                is_various = true;
            }

            // workaround for inline editing in mapping list
            var first = _mappings.FirstOrDefault();
            if (first != null)
                first.PropertyChanged += onCommentChangedInline;

            _selectedComments = common.Where(c => c != null).Where(c => c != "").OrderBy(c => c).ToList();
            _selectedComments.Add("");
            CommentsMenu = new ObservableCollection<MenuItemViewModel>(generateCommentsMenu());
            updateCommentsMenu();
        }


        private IEnumerable<MenuItemViewModel> generateCommentsMenu()
        {
            return Enumerable.Range(0, 0).Select(c =>
            {
                return new MenuItemViewModel { Text = "test", Tag = "test"};
            });
        }


        private void updateCommentsMenu()
        {
            CommentsMenu.Clear();
            var options = _selectedComments.Select(c => new MenuItemViewModel { Text = c, Tag = c }).ToList();
            //options.Select(d => CommentsMenu.Add(d));
            foreach(var comment in options)
            {
                CommentsMenu.Add(comment);
            }

        }


        // todo: add a pop-up list of selected comments
        private void onCommentChangedInline(object sender, PropertyChangedEventArgs e)
        {
            switch (e.PropertyName)
            {
                case "Comment":
                    _comment = (sender as MappingViewModel).Comment;
                    raisePropertyChanged("Comment");
                    break;
                default:
                    break;
            }
        }
    }
}
